# Weather_Vane

<h3 align="center">WeatherVane - Whisper GPT3 Codex & DALL-E 2 Open AI Hackathon</h3>
<br>
    This repo contains all the work for WeatherVanes team contribution in OpenAI's Whisper Hackathon
<br />


<p align="center">
<img src="https://github.com/Tex6298/Weather_Vane/blob/main/logo/weathervane4s.jpg" width="400" height="400" >
</p>

<!-- ABOUT THE PROJECT -->
## About The Project
<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

***Product Name***
WeatherVane (v1.0.0)

***Problem***
Regardless of the context time is always precious.
Presenting ideas is always necessary from starting small projects to guiding important decisions but making good presentations takes time.
Making an impact is done by creating a sensory experiences.

***Solution***
Using OpenAI GPT-3, DALL-E 2 and Murbet, we are created an automated presentation platform that will make your desired presentation with just the data you wish to present and some key words.

***How it works***
This is a high-level overview of how the project works. For more details, please refer to the [WeatherVane google collab]([https://miro.com/app/board/uXjVPNAvrXg=/](https://colab.research.google.com/drive/1BoNuDiHlC3eI82OoRqewlP6D6bdQJIvH?usp=sharing))

```mermaid
sequenceDiagram
    participant User
    participant FrontEnd
    participant WeatherVane
    participant Database API
    User->>FrontEnd: Enter Text
    FrontEnd->>FrontEnd: User enters presentation text
    FrontEnd->>WeatherVane: Send text for parsng to GPT-3
    WeatherVane->>WeatherVane:Generate images using DALL-E with text from GPT-3
    WeatherVane->>WeatherVane: Generate Music with Murbet with text from GPT-3
    WeatherVane->>WeatherVane: Generate Slides and preview using google Slide API
    WeatherVane->>FrontEnd: Display preview
    FrontEnd->>WeatherVane: Submit confirmaiton
    WeatherVane->>WeatherVane: Send everything to DALL-E for interpolation
    WeatherVane->>FrontEnd: Your presentation is underway
    WeatherVane->>Database API: Send data to database
    Database API->>User: email user that download is ready
```


