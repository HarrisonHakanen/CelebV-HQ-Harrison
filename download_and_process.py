"""
Downloader
"""

import os
import json
import cv2
import pandas as pd


def download(video_path, ytb_id, proxy=None):
    """
    ytb_id: youtube_id
    save_folder: save video folder
    proxy: proxy url, defalut None
    """
    if proxy is not None:
        proxy_cmd = "--proxy {}".format(proxy)
    else:
        proxy_cmd = ""
    if not os.path.exists(video_path):
        down_video = " ".join([
            "yt-dlp",
            proxy_cmd,            
            "https://www.youtube.com/watch?v=" + ytb_id, "--output",
            video_path, "--external-downloader", "aria2c",
            "--external-downloader-args", '"-x 16 -k 1M"'
        ])
        print(down_video)
        status = os.system(down_video)
        if status != 0:
            print(f"video not found: {ytb_id}")


def process_ffmpeg(raw_vid_path, save_folder, save_vid_name,
                   bbox, time):
                       
    """
    raw_vid_path:
    save_folder:
    save_vid_name:
    bbox: format: top, bottom, left, right. the values are normalized to 0~1
    time: begin_sec, end_sec
    """

    def secs_to_timestr(secs):
        hrs = secs // (60 * 60)
        min = (secs - hrs * 3600) // 60 # thanks @LeeDongYeun for finding & fixing this bug
        sec = secs % 60
        end = (secs - int(secs)) * 100
        return "{:02d}:{:02d}:{:02d}.{:02d}".format(int(hrs), int(min),
                                                    int(sec), int(end))

    def expand(bbox, ratio):
        top, bottom = max(bbox[0] - ratio, 0), min(bbox[1] + ratio, 1)
        left, right = max(bbox[2] - ratio, 0), min(bbox[3] + ratio, 1)

        return top, bottom, left, right

    def to_square(bbox):
        top, bottom, leftx, right = bbox
        h = bottom - top
        w = right - leftx
        c = min(h, w) // 2
        c_h = (top + bottom) / 2
        c_w = (leftx + right) / 2

        top, bottom = c_h - c, c_h + c
        leftx, right = c_w - c, c_w + c
        return top, bottom, leftx, right

    def denorm(bbox, height, width):
        top, bottom, left, right = \
            round(bbox[0] * height), \
            round(bbox[1] * height), \
            round(bbox[2] * width), \
            round(bbox[3] * width)

        return top, bottom, left, right

    print("\nINICIO - PROCESSAMENTO\n")
    out_path = os.path.join(save_folder, save_vid_name)

    cap = cv2.VideoCapture(raw_vid_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    top, bottom, left, right = to_square(
        denorm(expand(bbox, 0.02), height, width))
    start_sec, end_sec = time

    cmd = f"ffmpeg -i {raw_vid_path} -vf crop=w={right-left}:h={bottom-top}:x={left}:y={top} -ss {secs_to_timestr(start_sec)} -to {secs_to_timestr(end_sec)} -loglevel error {out_path}"
    os.system(cmd)    
    
    return out_path


def load_data(file_path):
    with open(file_path) as f:
        data_dict = json.load(f)

    for key, val in data_dict['clips'].items():
        save_name = key+".mp4"
        ytb_id = val['ytb_id']
        time = val['duration']['start_sec'], val['duration']['end_sec']

        bbox = [val['bbox']['top'], val['bbox']['bottom'],
                val['bbox']['left'], val['bbox']['right']]
        yield ytb_id, save_name, time, bbox


if __name__ == '__main__':
    
    videosData = pd.read_csv("videoData.csv",index_col=0)    
    json_path = 'celebvhq_info.json'  # json file path
    raw_vid_root = './downloaded_celebvhq/raw/'  # download raw video path
    processed_vid_root = './downloaded_celebvhq/processed/'  # processed video path
    proxy = None  # proxy url example, set to None if not use
    
    os.makedirs(raw_vid_root, exist_ok=True)
    os.makedirs(processed_vid_root, exist_ok=True)


    ultimoVideoFile = "ultimoVideo.txt"
        
    if os.path.isfile(ultimoVideoFile):
        
        ultimoVideoId = ""
        file1 = open(ultimoVideoFile, 'r')
        Lines = file1.readlines()                
        
        for line in Lines:
            ultimoVideoId = line.strip()
        
        
        if ultimoVideoId != "":
        
            indice_valor = videosData['VideoId'].eq(ultimoVideoId).idxmax()
            videosData = videosData.loc[indice_valor:]
        

    for row in videosData.itertuples(index=True, name='Pandas'):
        
        try:             
            vid_id = row[1]        
            save_vid_name = row[2]
            timeVideo = row[3]
            
            timeVideo = timeVideo.strip('()').split(',')
            timeVideo = tuple(float(valor) for valor in timeVideo)
            
            bbox = row[4]        
            bbox = eval(bbox)
                            
            raw_vid_path = os.path.join(raw_vid_root, vid_id + ".mp4.webm")
            
            f = open(ultimoVideoFile, "w")
            f.write(vid_id)
            f.close()
            
            
            download(raw_vid_path, vid_id, proxy)
            
            process_ffmpeg(raw_vid_path, processed_vid_root, save_vid_name, bbox, timeVideo)
            
            os.remove(raw_vid_path)
        except:
            print("Erro")
        
        '''
        with open('./ytb_id_errored.log', 'r') as f:
            lines = f.readlines()
        for line in lines:
            raw_vid_path = os.path.join(raw_vid_root, line + ".mp4")
            download(raw_vid_path, line)
        '''
        
    