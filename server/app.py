from flask import Flask, render_template, request, redirect, session, url_for
from dataloader import CustomtrainDataset
from model import proj_head
import torch
from torch.utils.data import DataLoader
import numpy as np
from text import text_embedding,Sentence_Embedding
import sys
import json
import re 
import torch.nn.functional as F


app = Flask(__name__, static_url_path='/')
app.secret_key = "your_secret_key"



@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')


# @app.route('/')
# def videoplayer():
#     # if not request.args.get('url'): return redirect('/')
#     return render_template('index.html', url=('testmp4.mp4'));


@app.route("/result", methods=['GET'])
def resulttest():
    return render_template('result.html')


@app.route("/video", methods=["POST"])
def result():
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
   
    if request.method == "POST":
        query = request.form['query']
        session['query'] = query

        query =[query]
        embd_dim = 256
        token_to_word_path = "mmv/dict.npy"
        word2vec_path = 'mmv/word2vec.pth'

        text_model = Sentence_Embedding(embd_dim, token_to_word_path, num_embeddings=66250,
                           word_embedding_dim=300, word2vec_path=word2vec_path,
                           max_words=16, output_dim=2048).to(device)

        queries_tensor = text_model.words_to_ids(query)

        with torch.no_grad():
            queries_tensor = queries_tensor.to(device)
            output = text_model.forward(queries_tensor, raw_text =False)
        
        output_np = output.cpu().numpy()

        text_data = output.squeeze(1)



        dataset = CustomtrainDataset('before_head_video.npy',
                                     'mmv/audio_before_head.npy',
                                     'mmv/text_before_head.npy')
        
        dataloader = DataLoader(dataset)
        
        
        model = proj_head().to(device)
        model.eval()   
        
        similarities = []
        model.load_state_dict(torch.load('mmv/Data_5120_3.pth', map_location=device))

        audio_input = torch.zeros(1,2048)

        for video, audio, text in dataloader:
            video = video.to(device)
            audio_input =  audio_input.to(device)
            text_input = text_data.to(device)

            video_feature, audio_feature, text_feature = model(video, audio_input, text_input)

            video_feature = F.normalize(video_feature,dim=-1)
            audio_feature = F.normalize(audio_feature,dim=-1)
            text_feature= F.normalize(text_feature,dim=-1)
            
            similarity1 = abs(torch.cosine_similarity(video_feature, audio_feature,dim=-1))
            similarity2 = abs(torch.cosine_similarity(video_feature, text_feature,dim=-1))
            similarity = (similarity1 + similarity2) / 2
            similarities.append(similarity)    # 비디오-오디오 쌍의 랭킹 계산
        similarities = torch.cat(similarities, dim=0)
        _, ranking = similarities.sort(descending=True)

        # cut top 10..
        # ranking = ranking[0:10]

        # video_name = []
        # with open('video_mapping.json', 'r') as json_file:
        #     video_mapping = json.load(json_file)

        # index = ranking.tolist()

        # for idx in index:
        #     video_name.append(video_mapping(str[idx]))
    
        # return render_template('videoresult.html', list=ranking)
        # cut top 10..
        ranking = ranking[0:10]

        # todo : ranking list의 size가 10이 안될떄 error handle 필요함.
        # size 가 10보다 안될때 자를떄 에러 핸들링 되는지까진 모르겠으니까 알아보3
        # sudo code example
        # if ranking size less than 10
        # maxSize = ranking.size
        # ranking = ranking[0:maxSize]


        # todo : 지금은 강제로 filename set해서 테스트하는거라서 그냥 하드코딩인데
        # ranking top 1의 metadata를 얻어올 수 있으면, 거기에 들어 있는 file name이 필요함
        # filename의 pre require는 staic 폴더 밑에 *.mp4형태로 존재해야함. 
        # 그래야 html의 video tag에서 실행 가능함. ( src 경로 )
        # 인덱스에 대한 동영상을 가져와야함 
        filename = ['testmp4.mp4','video4.mp4','video2.mp4','video3.mp4'] 
        start = [0,90,300,80,]
        # file name
        # start time, end time, score

        return render_template('videoresult.html', list=ranking, filename=filename)
    else:
        return redirect("/")
    



@app.route("/show_result", methods=["POST"])
def show_result():
    query = session.get('query')  # 세션에서 쿼리 가져오기
    if query is None:
        return redirect("/")

    # 세션에서 가져온 쿼리를 활용하여 결과 페이지를 표시합니다.

    return render_template('video.html', query=query)


if __name__ == '__main__':
    app.run()
