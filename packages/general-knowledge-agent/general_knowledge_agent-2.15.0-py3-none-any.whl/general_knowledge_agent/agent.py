import chromadb
import numpy as np
import pandas as pd
import openai

import re
import os

from datetime import datetime

from tqdm import tqdm
from typing import List

import langroid as lr

# Langchain dependencies
from langchain_community.embeddings import AzureOpenAIEmbeddings

from langchain.docstore.document import Document
from langchain.vectorstores.chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Base model structure
from cortex_cli.core.models.cortex_model import CortexModel
# Base inference structure
from general_knowledge_agent.inference import Conversation, LLM

# Threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


class GeneralKnowledgeAgent(CortexModel):

    ##################
    ### Properties ###
    ##################

    @property
    def debug(self):
        """
        Enables debug mode for the model.
        """
        return False
    

    @property
    def loaded_docs(self):
        """
        Returns True if documents have been loaded into the model.
        """
        return 'preprocessed_docs' in dir(self) and len(self.preprocessed_docs) > 0


    @property
    def has_chromadb(self):
        """
        Returns True if a ChromaDB has been created.
        """
        return os.path.isdir(self.params['chroma_directory'])


    ################################
    ### Initialization Functions ###
    ################################


    def initialize(self):
        """
        Sets input and output examples for the Cortex model.
        """
        input_example = pd.DataFrame({'Role': ['system'], 'Message': ['This is a test input']})

        # Set input and output examples
        self._set_input_output_examples(
            input_example, 
            np.array(['This is a test output'])
        )

        # Assign system messages
        self.prompt = self.params['prompt_template']
        self.inquiry = self.params['inquiry_template']
        self.followup = self.params['followup_template']

        self.is_deployment = False

        return 'Nearly Human General Knowledge Agent initialized successfully.'
    

    def setup_azure_openai_access(self):
        """
        Setup Azure OpenAI access via API keys.
        """
        # Shared access (Environment variables prefixed with `AZURE` are shared with Langroid, others are shared with LangChain)
        os.environ['AZURE_OPENAI_API_KEY'] = self.secrets_manager.get_secret(self.params['aoai_secret_name'])
        os.environ['OPENAI_API_KEY'] = os.environ['AZURE_OPENAI_API_KEY']

        # Setup access for Langroid
        os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'] = self.params['azure_deployment_name']
        os.environ['AZURE_OPENAI_MODEL_NAME'] = os.environ['AZURE_GPT_MODEL_NAME'] = self.params['azure_model_name']
        os.environ['AZURE_OPENAI_MODEL_VERSION'] = self.params['azure_model_version']
        os.environ['AZURE_OPENAI_API_VERSION'] = self.params['azure_api_version']
        os.environ['AZURE_OPENAI_API_BASE'] = self.params['azure_endpoint']

        openai.api_type = 'azure'
        openai.api_base = os.environ['AZURE_OPENAI_API_BASE']
        openai.api_version = os.environ['AZURE_OPENAI_API_VERSION']
        openai.api_key = os.environ['AZURE_OPENAI_API_KEY']

        os.environ['OPENAI_API_TYPE'] = openai.api_type
        os.environ['OPENAI_API_BASE'] = openai.api_base
        os.environ['OPENAI_API_VERSION'] = openai.api_version

        if 'config' not in dir(self):
            self.config = lr.ChatAgentConfig(
                llm=lr.language_models.AzureConfig(
                    api_base=os.environ['AZURE_OPENAI_API_BASE'],
                    deployment_name=os.environ['AZURE_OPENAI_DEPLOYMENT_NAME'],
                    model_name=os.environ['AZURE_OPENAI_MODEL_NAME'],
                    model_version=os.environ['AZURE_OPENAI_MODEL_VERSION'],
                    temperature=self.params['temperature'],
                    max_output_tokens=self.params['max_tokens']
                )
            )

        self.embeddings = AzureOpenAIEmbeddings(
            deployment=self.params['azure_embedding_deployment_name'],
            chunk_size=16
        )

        self._add_cleanup_var(['embeddings'])
        
        return 'Successfully configured Azure OpenAI access.'


    ##########################
    ### ChromaDB Functions ###
    ##########################


    def read_docs(self):
        """
        Loads documents from Cortex data into memory.
        """
        self.documents = []
        self.metadatas = []
        for file in self.cortex_data.files:
            if file.type in ['doc', 'docx', 'txt', 'pdf', 'rtf', 'md']:
                self.documents.append(file.load().strip())
                self.metadatas.append({
                    'file_name': file.name.rsplit('.', 1)[0]
                })
    

    def preprocess_docs(self):
        """
        Process documents for ChromaDB creation.
        """
        if self.has_chromadb:
            return 'Skipping document preprocessing, ChromaDB already exists.'
        
        # Split documents by NH delimiter
        recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=4096,
            chunk_overlap=0,
            length_function=len,
            separators=['\n\n', '\n']
        )

        new_texts = []
        new_metadatas = []

        pattern = r'\s+({.*?})'

        for i, doc in enumerate(self.documents):
            split = doc.split('--- NH SECTION DELIMITER ---')
            for j, section in enumerate(split):
                new_metadata = self.metadatas[i]
                
                # Select dict from first line of each section if it exists
                match = re.search(pattern, section.split('\n')[0])
                if match:
                    try:
                        metadata = eval(match.group(0))
                        # Handle exceptions
                        if type(metadata) != dict:
                            raise Exception('Invalid dictionary format')
                        
                        if len(metadata.keys()) == 0:
                            raise Exception('Empty dictionary')
                        
                        if 'section_images' in metadata.keys():
                            metadata['section_images'] = ','.join(metadata['section_images'])
                                            
                        metadata.update(new_metadata)

                        # Add expanded metadata if additional found
                        new_metadatas.append(metadata)

                        # Remove original metadata text from section
                        split[j] = '\n'.join(section.split('\n')[1:])

                        continue
                    except Exception as e:
                        # Invalid dictionary format
                        print(f'Invalid dictionary input for context section:\n{section}\n{e}')

                # Add default document metadata if none found
                new_metadatas.append(new_metadata)
            # Add documents in bulk
            new_texts.extend(split)
        recurse_documents = recursive_splitter.create_documents(new_texts, new_metadatas)

        ### Handle associated prompts ###
        original_texts = []
        embedding_texts = []
        metadatas = []

        for doc in recurse_documents:
            original_texts.append(doc.page_content)
            embedding_texts.append(self.strip_text(doc.page_content))
            metadatas.append(doc.metadata)
            if 'associated_prompts' in doc.metadata.keys():
                for associated_prompt in doc.metadata['associated_prompts']:
                    original_texts.append(doc.page_content)
                    embedding_texts.append(associated_prompt)
                    metadatas.append(doc.metadata)
                
                # Remove list metadata
                del doc.metadata['associated_prompts']
        #################################


        ### Embed documents ###
        embeddings, error_count = self.safe_embed(embedding_texts)
        #######################

        self.preprocessed_docs = (original_texts, metadatas, embeddings)

        if self.debug:
            with open('chunks.txt', 'w') as f:
                f.write('\n\n-------------------------------------------------------\n\n\n\n'.join([doc.page_content for doc in recurse_documents]))

            with open('embeddings.txt', 'w') as f:
                f.write('\n\n-------------------------------------------------------\n\n\n\n'.join([str(x) for x in embeddings]))
            
            with open('final_chunks.txt', 'w') as f:
                f.write('\n\n-------------------------------------------------------\n\n\n\n'.join(original_texts))

        self._add_cleanup_var(['documents', 'metadatas'])

        print(f'Encountered {error_count} embedding errors.')

        return f'Encountered {error_count} embedding errors.'


    def strip_text(self, text: str) -> str:
        """
        Strips text of all non-alphanumeric characters.
        """
        # Matches any number of '#' characters at the beginning of the string
        hash_pattern = re.compile(r'^#+\s*')
        result1 = re.sub(hash_pattern, '', text)
        # Matches any number of '/*' characters
        star_pattern = re.compile(r'\*')
        result2 = re.sub(star_pattern, '', result1)
        # Matches '-' characters on their own line
        dash_pattern = re.compile(r'^\s*-\s*', re.MULTILINE)
        result3 = re.sub(dash_pattern, '', result2)

        return result3

    
    def safe_embed(self, documents: List[str], max_workers: int=1, progress_bar: bool=True) -> (List[np.ndarray], int):
        """
        Generate safe embeddings from documents. Will embed text 9 times and select the most common embeddings.
        """
        final_embeddings = []
        embeddings = []

        total_embeddings = 9

        batch_results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for i in range(total_embeddings):
                batch_results.append(executor.submit(self.embeddings.embed_documents, documents))
            for result in tqdm(as_completed(batch_results), desc='Running embedding batches', disable=not progress_bar):
                embeddings.append(np.array(result.result()))

        error_count = 0
        
        for i in range(len(embeddings[0])):
            emb_dict = {}
            for j in range(len(embeddings)):
                sum = embeddings[j][i].sum()

                if sum in emb_dict:
                    emb_dict[sum].append(embeddings[j][i])
                else:
                    emb_dict[sum] = [embeddings[j][i]]
            
            best_key = None
            max_count = 0

            if len(emb_dict.keys()) > 1:
                error_count += 1
            for k, v in emb_dict.items():
                count = len(v)

                if best_key is None or count > max_count:
                    best_key = k
                    max_count = count
            
            final_embeddings.append(emb_dict[best_key][0].tolist())
        
        return (final_embeddings, error_count)


    def fine_tune(self):
        """
        Creates a ChromaDB from the documents in Cortex data.
        """
        print('Fine tuning model...')

        save_chroma_db = not self.has_chromadb

        if self.has_chromadb:
            client_local = chromadb.PersistentClient(self.params['chroma_directory'])
            collection_local = client_local.get_collection('nearlyhuman')

            local_data = collection_local.get(include=['embeddings', 'documents', 'metadatas'])

            self.preprocessed_docs = (local_data['documents'], local_data['metadatas'], local_data['embeddings'])

        if not self.loaded_docs:
            return 'No Cortex documents found to fine tune on.'
        
        self._add_cleanup_var(['db'])

        documents, metadatas, embeddings = self.preprocessed_docs

        client = chromadb.PersistentClient(path=self.params['chroma_directory'])
        if save_chroma_db:
            collection = client.create_collection(name="nearlyhuman", metadata={"hnsw:space": "cosine"})

            collection.add(
                ids=[str(i) for i in range(len(documents))],
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings
            )
        
        self.db = Chroma(
            collection_name='nearlyhuman',
            client=client,
            collection_metadata={"hnsw:space": "cosine"}
        )

        # Only save chroma_db if we generated a new chroma_db and we're not in deployment mode
        if save_chroma_db and not self.is_deployment:
            file_paths = []

            # Get files from pipeline run
            for root, dirs, files in os.walk(self.params['chroma_directory']):
                for file in files:
                    file_paths.append(os.path.join(root, file))

            # Upload files to Cortex
            self.cortex_data.upload_to_cortex(file_paths)

        return 'ChromaDB created successfully.'


    def fine_tune_messages(self, conversation: Conversation, inquiry: str) -> Conversation:
        """
        Formats messages for model ingestion.
        """

        last_idx = len(conversation.messages) - 1
        last_interaction = conversation.llm_messages[last_idx]
        if last_interaction.role == 'user':
            if len(conversation.documents) == 0:
                fallback_context = 'NO relevent documents found within knowledgebase.'

                # Format appropriate system prompt to user message and document context
                last_interaction.content = self.prompt.format(
                    instruction=last_interaction.content,
                    context=fallback_context
                )
            else:
                # Include document context on last user message
                last_interaction.content = self.prompt.format(
                    instruction=last_interaction.content,
                    context=self.format_document_context(conversation.documents)
                )

            # Update conversation
            conversation.llm_messages[last_idx] = last_interaction

        return conversation
    

    def format_document_context(self, lst: List[Document]):
        # Format document contents with section names for LLM interpretation
        if 'expose_section_headers' in self.params and self.params['expose_section_headers']:
            contents = [f'Document Section: {doc.metadata["section_name"]}\n{doc.page_content}' if (doc.metadata and 'section_name' in doc.metadata) else doc.page_content for doc in lst]
        else:
            contents = [doc.page_content for doc in lst]
        context = '\n\n\n'.join([content for content in contents])
        return context


    def get_context(self, message: str, k: int=10):
        """
        Grabs context from the ChromaDB based on a user's latest message.
        """
        # Get safe embedding for query message
        embeddings = self.safe_embed([message], progress_bar=False)[0]

        confident_docs = self.db.similarity_search_by_vector_with_relevance_scores(embeddings, k=k)
        docs = []

        # Set relevance scores within document metadata
        for doc, conf in confident_docs:
            doc.metadata['relevance'] = int((1 - round(conf, 2)) * 100)
            if doc.metadata['relevance'] > self.params['context_dropout_threshold'] * 100:
                docs.append(doc)

        # Return empty list of no relavent documents found
        if len(docs) == 0:
            return docs
        
        removed_duplicates = self.remove_duplicate_doc_texts(docs)

        # Fit documents to size
        fitted_docs = self.fit_to_size([doc.page_content for doc in removed_duplicates])

        # Return documents in reversed order (Helps LLM attention span)
        return docs[:len(fitted_docs)][::-1]


    @staticmethod
    def remove_duplicate_doc_texts(lst: List[Document]) -> List[Document]:
        """
        Removes duplicate documents from a list based on their page content.
        """

        new_lst = []

        for i, doc in enumerate(lst):
            for compare in lst:
                # If duplicate page contents are found and documents are fundimentally different
                if doc.page_content == compare.page_content and doc != compare:
                    continue
            new_lst.append(doc)
        return new_lst


    @staticmethod
    def fit_to_size(lst: List[str], limit=8192) -> List[str]:
        """
        Takes in lst of strings and returns join of strings
        up to `limit` number of chars (no substrings)

        :param lst: (list)
            list of strings to join
        :param limit: (int)
            optional limit on number of chars, default 50
        :return: (list)
            string elements joined up until length of 50 chars.
            No partial-strings of elements allowed.
        """
        for i in range(len(lst)):
            new_join = lst[:i+1]
            if len('\n\n\n'.join(new_join)) > limit:
                return lst[:i]
        return lst
    

    def replace_image_url_format(self, message: str) -> str:
        """
        Matches URLs in the format [alt text](url) and replaces them with ![alt text](url)
        when http, https, and www are not found in the URL. Allows for proper image rendering
        """
        regex = r'(!?\[)([^]]+)(\]\([^)]+\))'

        matches = re.finditer(regex, message)

        for match in matches:
            full_match = match.group(0)
            
            # Check if the URL part does not contain '!, 'http', 'https', or 'www'
            if not re.search(r'!|http[s]?://|www\.', full_match):
                message = message.replace(full_match, f'!{full_match}')
        
        return message
    

    ###########################
    ### Follow-up Functions ###
    ###########################


    def build_followup_model(self):
        """
        Builds a follow-up model for the agent using Naive Bayes.
        """

        if 'followup_training_filename' in self.params and 'enable_followup' in self.params and not self.params['enable_followup']:
            return 'Follow-up system disabled or missing required parameters.'
        
        # Load the training data from the excel file
        training_data = self.cortex_data.find_file(self.params['followup_training_filename']).load()
        
        # Split the data into features (text) and target (class)
        X = training_data['text']
        y = training_data['class']
        
        # Convert the text data into numerical features using CountVectorizer
        self.vectorizer = CountVectorizer()
        X_vectorized = self.vectorizer.fit_transform(X)
        
        # Train the Naive Bayes model
        model = MultinomialNB()
        model.fit(X_vectorized, y)
        
        # Save the trained model for future use
        self.followup_model = model

        # Print accuracy of the model
        accuracy = int(model.score(X_vectorized, y) * 100)
        print(f'Follow-up model trained with accuracy: {accuracy}%')
        return f'Follow-up model trained with accuracy: {accuracy}%'


    ############################
    ### Prediction Functions ###
    ############################


    def predict(self, model_inputs: pd.DataFrame) -> pd.DataFrame:
        """
        Runs inference on a dataframe of messages.
        """
        response = 'Unable to complete the request to Nearly Human General Knowledge Agent.'

        ### Inquiry ###

        inquiry = None

        roles = model_inputs['Role'].to_list()
        messages = model_inputs['Message'].to_list()

        inquiry_message = self.inquiry.format(
            user_prompt=messages[-1],
            conversation_history='\n'.join([f'{role}: {message}' for role, message in zip(roles[1:-1], messages[1:-1]) if role == 'user'])
        )

        # Initialize inquiry conversation
        inquiry_conversation = Conversation(
            roles = ['system', 'user'],
            messages = [self.params['inquiry_system_prompt'], inquiry_message]
        )

        # Create inquiry agent from config and inference model for a response
        inquiry = LLM(conversation=inquiry_conversation, agent_config=self.config).infer()
        ################

        # Predict followup
        needs_follow_up = False

        if self.params['enable_followup']:
            text_counts = self.vectorizer.transform([inquiry])
            needs_follow_up = self.followup_model.predict(text_counts)[0] == 1

        print('-' * 30)
        print(f'Inquiry: {inquiry}')
        print(f'Follow-up prediction: {needs_follow_up}')
        print('-' * 30)

        # Initialize inference variables
        response = None
        conversation = None
        roles = []
        messages = []

        # Get inquiry docs
        docs = self.get_context(inquiry if inquiry else last_interaction.message)

        if needs_follow_up:
            # Setup followup system prompt
            if 'followup_system_prompt' in self.params:
                roles.append('system')
                messages.append(self.params['followup_system_prompt'])

            followup_message = self.followup.format(
                user_prompt=inquiry,
                context=self.format_document_context(docs)
            )

            # Initialize followup conversation
            conversation = Conversation(
                roles = ['system', 'user'],
                messages = [self.params['followup_system_prompt'], followup_message],
                documents = docs
            )

            # Create followup agent from config and inference model for a response
            response = LLM(conversation=conversation, agent_config=self.config).infer()
        else:
            # Setup system prompt
            if self.params and self.params['system_prompt']:
                roles.append('system')
                messages.append(self.params['system_prompt'])

            # Add user messages to conversation
            roles.extend(model_inputs['Role'].to_list())
            messages.extend(model_inputs['Message'].to_list())

            # Initialize main conversation
            conversation = Conversation(
                roles = roles, 
                messages = messages,
                documents = docs
            )
            conversation = self.fine_tune_messages(conversation, inquiry)

            # Create conversation agent from config and inference model for a response
            response = LLM(conversation=conversation, agent_config=self.config).infer()

        documents, metadatas = [], []
        for doc in conversation.documents:
            documents.append(doc.page_content)
            metadatas.append(doc.metadata)

        # Regex correction for some image url format errors
        response = self.replace_image_url_format(response)

        # Format response into a DataFrame and return
        result = pd.DataFrame({
            'Message': [response],
            'Role': ['assistant'],
            'Documents': [documents],
            'Metadatas': [metadatas]
        })
        return result


    def set_input_output_examples(self) -> str:
        """
        Single evaluation point for the model. Used to set input output examples.
        """
        conversation = Conversation(
            roles=['user'], 
            messages=['My drawer has unsent files']
        )
        
        input_example = conversation.to_pandas()
        output_example = self.predict(input_example)

        # Remove array columns from output (Bug caused by MLFlow)
        output_example = output_example.drop(columns=['Documents', 'Metadatas'])

        # Set input and output examples
        self._set_input_output_examples(
            input_example, 
            output_example
        )

        # Add interaction to conversation
        conversation.add_interaction('assistant', output_example['Message'].iloc[0])
       
       # Print response for debugging
        conversation_str = conversation.to_str()
        print(conversation_str)

        # Set deployment status after successful prediction
        self.is_deployment = True

        return conversation_str


    ##################################
    ### Batch Evaluation Functions ###
    ##################################

    
    def batch_prediction(self, df: pd.DataFrame, batch_size: int, batch_idx: int):
        """
        Takes list of questions, processes them, runs inference on each question, then returns batch.
        Param: List of Questions
        """

        # For each question in the current batch
        for i in range(df.shape[0]):
            global_idx = batch_idx * batch_size + i
            response = self.predict(df.loc[i:i, :])
            self.df.loc[global_idx:global_idx, 'Answer'] = response['Message'].values[0]


    def thread_batch_eval(self, batch_size: int=1, max_workers: int=1):
        """
        Threads batch inferences using predict function. 
        Param: List of Questions, Batch Size. (Set to 1 by default)
        """
        batch_results = []

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            
            for i in range(0, self.df.shape[0], batch_size):
                batch_input = self.df.iloc[i : i + batch_size].reset_index(drop=True)
                batch_results.append(executor.submit(self.batch_prediction, batch_input, batch_size, i))
            for result in as_completed(batch_results):
                result.result()


    def thread_batch_eval_pipe(self, excel_file: str='data/eval/evaluation.csv'):
        """
        Kicks off batch evaluation pipeline.
        """
        try:
            self.df = pd.read_csv(excel_file)
            self.df = self.df.astype({'Answer': 'str'})
            self.thread_batch_eval()
            file_name = f'data/eval/v{self.params["model_version"]}_{datetime.now().strftime("%m-%d-%Y_%H:%M:%S")}.csv'
            self.df.to_csv(file_name, index=False)
            self._add_cleanup_var('df')

            self.cortex_data.upload_to_cortex(file_name)
        except FileNotFoundError:
            return 'Skipping Batch Evaluation, CSV File not found.'
    
        except KeyError:
            return 'Couldn\'t deconstruct CSV, please check formatting.'
