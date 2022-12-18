from __future__ import print_function
import os

import openai
import requests as r
from PIL import Image
from io import BytesIO
import httpx
import json
import numpy as np
from sentence_transformers import SentenceTransformer


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import ffmpeg

SCOPES = ['https://www.googleapis.com/auth/presentations']
creds =None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

openai.api_key = st.secrets["openai_api"]

minilm = SentenceTransformer('all-MiniLM-L6-v2')


mubert_tags_string = 'tribal,action,kids,neo-classic,run 130,pumped,jazz / funk,ethnic,dubtechno,reggae,acid jazz,liquidfunk,funk,witch house,tech house,underground,artists,mystical,disco,sensorium,r&b,agender,psychedelic trance / psytrance,peaceful,run 140,piano,run 160,setting,meditation,christmas,ambient,horror,cinematic,electro house,idm,bass,minimal,underscore,drums,glitchy,beautiful,technology,tribal house,country pop,jazz & funk,documentary,space,classical,valentines,chillstep,experimental,trap,new jack swing,drama,post-rock,tense,corporate,neutral,happy,analog,funky,spiritual,sberzvuk special,chill hop,dramatic,catchy,holidays,fitness 90,optimistic,orchestra,acid techno,energizing,romantic,minimal house,breaks,hyper pop,warm up,dreamy,dark,urban,microfunk,dub,nu disco,vogue,keys,hardcore,aggressive,indie,electro funk,beauty,relaxing,trance,pop,hiphop,soft,acoustic,chillrave / ethno-house,deep techno,angry,dance,fun,dubstep,tropical,latin pop,heroic,world music,inspirational,uplifting,atmosphere,art,epic,advertising,chillout,scary,spooky,slow ballad,saxophone,summer,erotic,jazzy,energy 100,kara mar,xmas,atmospheric,indie pop,hip-hop,yoga,reggaeton,lounge,travel,running,folk,chillrave & ethno-house,detective,darkambient,chill,fantasy,minimal techno,special,night,tropical house,downtempo,lullaby,meditative,upbeat,glitch hop,fitness,neurofunk,sexual,indie rock,future pop,jazz,cyberpunk,melancholic,happy hardcore,family / kids,synths,electric guitar,comedy,psychedelic trance & psytrance,edm,psychedelic rock,calm,zen,bells,podcast,melodic house,ethnic percussion,nature,heavy,bassline,indie dance,techno,drumnbass,synth pop,vaporwave,sad,8-bit,chillgressive,deep,orchestral,futuristic,hardtechno,nostalgic,big room,sci-fi,tutorial,joyful,pads,minimal 170,drill,ethnic 108,amusing,sleepy ambient,psychill,italo disco,lofi,house,acoustic guitar,bassline house,rock,k-pop,synthwave,deep house,electronica,gabber,nightlife,sport & fitness,road trip,celebration,electro,disco house,electronic'
mubert_tags = np.array(mubert_tags_string.split(','))
mubert_tags_embeddings = minilm.encode(mubert_tags)


email = "martyn.ben.ami@gmail.com" #@param {type:"string"}


r = httpx.post('https://api-b2b.mubert.com/v2/GetServiceAccess',
    json={
        "method":"GetServiceAccess",
        "params": {
            "email": email,
            "license":"ttmmubertlicense#f0acYBenRcfeFpNT4wpYGaTQIyDI4mJGv5MfIhBFz97NXDwDNFHmMRsBSzmGsJwbTpP1A6i07AXcIeAHo5",
            "token":"4951f6428e83172a4f39de05d5b3ab10d58560b8",
            "mode": "loop"
        }
    })

rdata = json.loads(r.text)
assert rdata['status'] == 1, "probably incorrect e-mail"
pat = rdata['data']['pat']
print(f'Got token: {pat}')


def query_image_creation_api(query: str, image_size:str = "256x256" ) -> Image:
    response = openai.Image.create(
    prompt=query,
    n=1,
    size=image_size
    )
    image_url = response['data'][0]['url']
    #response = r.get(image_url, timeout=5)
    #img = Image.open(BytesIO(response.content))
    return image_url

def query_text_completion_api(query: str, model_key = "text-davinci-003", num_tokens = 500, temp=0.7):
    template = f""" You are to convert a given topic_query to a list of prompts that are both descriptive and representative of the topic query
                    for the purpose of querying music and image generation services
                    This is the Query: {query}

    """
    resp = openai.Completion.create(
    model=model_key,
    prompt=template,
    max_tokens=num_tokens,
    temperature=temp
    )
    return resp

def query_bullet_point_api(query: str, model_key = "text-davinci-003", num_tokens = 500, num_bullet_point=2, temp=0.7) -> list:
    template = f""" You are to convert a given topic_query to a list of {num_bullet_point} bullet points that are both descriptive and represnetative of the topic query
     for the purpose of a slide show, they can be fun facts, interesting observations, or questions
        This is the Query: {query}

    """
    response = openai.Completion.create(
    prompt=query,
    max_tokens=num_tokens,
    temperature=temp,
    frequency_penalty=0,
    presence_penalty=0
    )
    bullet_points = response['choices'][0]['text'].replace("\n", "").split(".")
    return bullet_points[:num_bullet_point]





def get_track_by_tags(tags, pat, duration, maxit=20, autoplay=False, loop=False):
  if loop:
    mode = "loop"
  else:
    mode = "track"
  r = httpx.post('https://api-b2b.mubert.com/v2/RecordTrackTTM',
      json={
          "method":"RecordTrackTTM",
          "params": {
              "pat": pat,
              "duration": duration,
              "tags": tags,
              "mode": mode
          }
      })

  rdata = json.loads(r.text)
  assert rdata['status'] == 1, rdata['error']['text']
  trackurl = rdata['data']['tasks'][0]['download_link']
  '''
  print('Generating track ', end='')
  for i in range(maxit):
      r = httpx.get(trackurl)
      if r.status_code == 200:
          #Audio(trackurl, autoplay=autoplay)
          break
      time.sleep(1)
      print('.', end='')
  '''
  return trackurl
def find_similar(em, embeddings, method='cosine'):
    scores = []
    for ref in embeddings:
        if method == 'cosine':
            scores.append(1 - np.dot(ref, em)/(np.linalg.norm(ref)*np.linalg.norm(em)))
        if method == 'norm':
            scores.append(np.linalg.norm(ref - em))
    return np.array(scores), np.argsort(scores)

def get_tags_for_prompts(prompts, top_n=3, debug=False):
    prompts_embeddings = minilm.encode(prompts)
    ret = []
    for i, pe in enumerate(prompts_embeddings):
        scores, idxs = find_similar(pe, mubert_tags_embeddings)
        top_tags = mubert_tags[idxs[:top_n]]
        top_prob = 1 - scores[idxs[:top_n]]
        if debug:
            print(f"Prompt: {prompts[i]}\nTags: {', '.join(top_tags)}\nScores: {top_prob}\n\n\n")
        ret.append((prompts[i], list(top_tags)))
    return ret

def generate_track_by_prompt(prompt, duration, loop=False):
  _, tags = get_tags_for_prompts([prompt,])[0]
  try:
    return get_track_by_tags(tags, pat, duration, autoplay=True, loop=loop)
  except Exception as e:
    print(str(e))


def create_presentation(title):
    """
        Creates the Presentation the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """
    
    # pylint: disable=maybe-no-member
    try:
        service = build('slides', 'v1', credentials=creds)

        body = {
            'title': title
        }
        presentation = service.presentations() \
            .create(body=body).execute()
        print(f"Created presentation with ID:"
              f"{(presentation.get('presentationId'))}")
        return presentation

    except HttpError as error:
        print(f"An error occurred: {error}")
        print("presentation not created")
        return error

def create_slide(presentation_id, page_id, n):
    """
    Creates the Presentation the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.\n
    """
    #creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    try:
        service = build('slides', 'v1', credentials=creds)
        # Add a slide at index 1 using the predefined
        # 'TITLE_AND_TWO_COLUMNS' layout and the ID page_id.
        requests = [
            {
                'createSlide': {
                    'objectId': page_id,
                    'insertionIndex': n,
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_AND_TWO_COLUMNS'
                    }
                }
            }
        ]

        # If you wish to populate the slide with elements,
        # add element create requests here, using the page_id.

        # Execute the request.
        body = {
            'requests': requests
        }
        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        create_slide_response = response.get('replies')[0].get('createSlide')
        print(f"Created slide with ID:"
              f"{(create_slide_response.get('objectId'))}")
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Slides not created")
        return error

    return response

def create_image(query, presentation_id, page_id):
    """
        Creates images the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """

    #creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    image_url = query_image_creation_api(query, image_size="1024x1024")
    try:
        service = build('slides', 'v1', credentials=creds)
        # pylint: disable = invalid-name
        # pylint: disable=invalid-name
        requests = []
        requests.append({
            "updatePageProperties": {
                "objectId": page_id,
                "pageProperties": {
                "pageBackgroundFill": {
                    "stretchedPictureFill": {
                    "contentUrl": image_url
                    }
                }
                },
                "fields": "pageBackgroundFill"
            }
        })

    # Execute the request.
        body = {
            'requests': requests
        }
        response = service.presentations() \
            .batchUpdate(presentationId=presentation_id, body=body).execute()
        #create_image_response = response.get('replies')[0].get('createImage')
        #print(f"Created image with ID: "
              #f"{(create_image_response.get('objectId'))}")

        return response
    except HttpError as error:
        print(f"An error occurred: {error}")
        print("Images not created")
        return error

        
    

def create_video(query, presentation_id, page_id):
    """
        Creates video the user has access to.
        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """

    #creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    AUDIO_FILE_URL = generate_track_by_prompt(query, 30)
    #add auido as video files
    #download auido file
    #upload audio file to google drive

    service = build('slides', 'v1', credentials=creds)

    requests = []


    requests.append({
        'createVideo': {'source': AUDIO_FILE_URL,
                        'id': presentation_id,
                        'elementProperties':
                        {'pageObjectId': page_id,}
                        }
                    })

# Execute the request.
    body = {
        'requests': requests
    }
    response = service.presentations() \
        .batchUpdate(presentationId=presentation_id, body=body).execute()
    create_video_response = response.get('replies')[0].get('createVideo')
    print(f"Created video with ID: "
            f"{(create_video_response.get('objectId'))}")

    return response

    

    




# presentation = create_presentation("test6ab1")


# pres_id = presentation.get('presentationId')
# create_slide(pres_id, n)
# create_image(summary, pres_id, n)


#create_video("Dogs playing poker with a wolf", pres_id, "page1") Does not work
#trackurl = generate_track_by_prompt("Dogs playing poker with a wolf", duration=30)
