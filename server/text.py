from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize, regexp_tokenize
import re
import numpy as np
import time
from tqdm import notebook
from transformers import AutoTokenizer
from torch.nn.utils.rnn import pad_sequence
import nltk
nltk.download('stopwords')
nltk.download('punkt')
import gensim
from gensim.models.keyedvectors import KeyedVectors
import torch as th
import torch.nn as nn
import torch.nn.functional as F
import json


class Sentence_Embedding(nn.Module):
    def __init__(self, embd_dim, token_to_word_path, num_embeddings=66250, word_embedding_dim=300, word2vec_path='', max_words=16, output_dim=2048, stopwords=None):
        super(Sentence_Embedding, self).__init__()
        if word2vec_path:
            self.word_embd = nn.Embedding.from_pretrained(th.load(word2vec_path))
        else:
            self.word_embd = nn.Embedding(num_embeddings, word_embedding_dim)
        self.fc1 = nn.Linear(word_embedding_dim, output_dim)
        self.fc2 = nn.Linear(output_dim, embd_dim)
        self.word_to_token = {}
        self.max_words = max_words
        token_to_word = np.load(token_to_word_path)
        self.stopwords = stopwords
        for i, t in enumerate(token_to_word):
            self.word_to_token[t] = i + 1

    def _zero_pad_tensor_token(self, tensor, size):
        if len(tensor) >= size:
            return tensor[:size]
        else:
            zero = th.zeros(size - len(tensor)).long()
            return th.cat((tensor, zero), dim=0)

    def is_cuda(self):
        return self.fc1.bias.is_cuda

    def _split_text(self, sentence):
        w = re.findall(r"[\w']+", str(sentence).lower())
        if self.stopwords:
            w = [word for word in w if word not in self.stopwords]
        return w

    def _words_to_token(self, words):
        words = [self.word_to_token[word] for word in words if word in self.word_to_token]
        if words:
            we = self._zero_pad_tensor_token(th.LongTensor(words), self.max_words)
            return we
        else:
            return th.zeros(self.max_words).long()

    def words_to_ids(self, x):
        split_x = [self._words_to_token(self._split_text(sent)) for sent in x]
        return th.stack(split_x, dim=0)

    def forward(self, x, raw_text=False):
        if raw_text:
            x = self.words_to_ids(x)
        with th.no_grad():
            x = self.word_embd(x)
        x = F.relu(self.fc1(x), inplace=True)
        x1 = th.max(x, dim=1, keepdim=True)[0]
        #x2 = F.relu(self.fc2(x1), inplace=True)
        return x1

    def vid_to_text(self, x):
        data_vid_to_text = []
        for i in range(0, len(x)):
            dict = {}
            data_vid_to_text.append(dict)
            data_vid_to_text[i]['vid'], data_vid_to_text[i]['query'] = x[i]['vid'], x[i]['query']
        return data_vid_to_text


class text_embedding:
    def __init__(self, Video_file_name, embd_dim=256):
        self.Video_file_name = Video_file_name
        self.embd_dim = embd_dim
          
            
    def build_Sentence_Embedding_instance(self): # Sentence_Embedding 클래스 인스턴스 생성  
        embd_dim = self.embd_dim
        token_to_word_path = "./mmv/dict.npy"
        word2vec_path = "./mmv/word2vec.pth"
        device = th.device("cuda" if th.cuda.is_available() else "cpu")
        model = Sentence_Embedding(embd_dim, \
                                   token_to_word_path, \
                                   num_embeddings=66250, \
                                   word_embedding_dim=300, \
                                   word2vec_path=word2vec_path, \
                                   max_words=16, \
                                   output_dim=2048).to(device)
        return model
        
    
    def text_embedding(self, preprocessed_data):
        # 모델에 입력하여 임베딩 벡터 얻기
        embedding_vector1 = self.model.forward(preprocessed_data, raw_text=False)
        detached_tensor = embedding_vector1.detach()
        array_data = detached_tensor.numpy()
        return array_data
        
        
    def extract(self, model, name_query_path, before_head_text):
        
        for i in range(len(self.Video_file_name)):
            with open(name_query_path.format(i)) as json_file:
                text_data = json.load(json_file)

                # dict화 해서 query & vid만 남게
                preprocessed_data = model.vid_to_text(text_data)

                # 입력받은 문장들을 단어로 분리한 후 _word_to_token으로 각 문장을 토큰으로 변환
                preprocessed_data = model.words_to_ids(preprocessed_data)

                # 전처리된 데이터를 device로 이동
                device = th.device("cuda" if th.cuda.is_available() else "cpu")  # 장치 설정
                input_word = preprocessed_data.to(device)

                input_word = th.from_numpy(inpnut_word)
                input_word = input_word.to(device)

                text_before_head = text_embedding(input_word)
                np.save(before_head_text.format(i), text_before_head)
                
                
    def extract_test(self, model, query, before_head_text='저장경로 입력'):
        text_data = [{'vid': 'input_query', 'query': query}]

        # dict화 해서 query & vid만 남게
        preprocessed_data = model.vid_to_text(text_data)

        # 입력받은 문장들을 단어로 분리한 후 _word_to_token으로 각 문장을 토큰으로 변환
        preprocessed_data = model.words_to_ids(preprocessed_data)

        # 전처리된 데이터를 device로 이동
        device = th.device("cuda" if th.cuda.is_available() else "cpu")  # 장치 설정
        input_word = preprocessed_data.to(device)

        # input_word = th.from_numpy(input_word)
        input_word = input_word.to(device)

        text_before_head = text_embedding(input_word)
        np.save(before_head_text, text_before_head)
