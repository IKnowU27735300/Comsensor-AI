</head>
<body>
    <h1>Comsensor-AI</h1>
    <p>Detect the Abusing Words And Beeping It (Can Be implemented in live streaming applications)</p>
    <h2>Overview</h2>
    <p>This project is designed to detect abusive words in audio streams and replace them with a beep sound. It can be used in live streaming applications to ensure a safe and respectful environment.</p>
    </ul>
    <h2>Functionality</h2>
    <p>The main functionalities of the application include:</p>
    <ul>
        <li>Recording audio from the microphone.</li>
        <li>Converting recorded audio to text using speech recognition.</li>
        <li>Censoring specified abusive words from the text.</li>
        <li>Converting the censored text back to speech.</li>
        <li>Adding beep sounds to the original audio where abusive words were detected.</li>
    </ul>
    <h2>Usage</h2>
    <p>To use the application:</p>
    <ol>
        <li>Run the <code>COMS SENSOR.py</code> script.</li>
        <li>Select the option to go live.</li>
        <li>Input the words you want to censor, separated by commas.</li>
        <li>Follow the prompts to record audio and process it.</li>
    </ol>
    <h2>Requirements</h2>
    <p>Make sure to have the following Python packages installed:</p>
    <ul>
        <li><code>pyaudio</code></li>
        <li><code>wave</code></li>
        <li><code>speech_recognition</code></li>
        <li><code>pydub</code></li>
        <li><code>gtts</code></li>
    </ul>
    <h2>License</h2>
    <p>This project is open-source and available for modification and distribution under the terms of the MIT License.</p>
</body>
</html>
