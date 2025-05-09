from autobahn.twisted.component import Component, run
from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.util import sleep
import random
import os
from alpha_mini_rug.speech_to_text import SpeechToText
from alpha_mini_rug import perform_movement
from google import genai

# Initialize Gemini API with API key
client = genai.Client(api_key="to be added here")
chat = client.chats.create(model="gemini-2.0-flash")

# Create an instance of the SpeechToText class (speech to text)
audio_processor = SpeechToText()

# Adjusting parameters
audio_processor.silence_time = 0.5  # Time to stop recording audio
audio_processor.silence_threshold2 = 150  # Sound below this value is considered silence
audio_processor.logging = True  

# Define time delta for animations
delta_t = 3000  # 1000 ms = 1 sec

def proprio(frame):
    """Handles proprioceptive data and logs every few seconds."""
    print("Proprioceptive data received:", frame)

@inlineCallbacks
def say_animated(session, text, frame_type=None):
    """
    Sends movement frames and speaks text using perform_movement().
    The following frame sets are defined:
      - Default sets: frames, frames2, frames3
      - framespreend: used for game restart prompts (when frame_type=="preend")
      - framesend: used for ending prompts (when frame_type=="end")
    If frame_type is not specified, a random default frame set is chosen.
    """
    # Default key frame sets
    frames = [
        {"time": 0.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": 0.0,
                                          "body.arms.right.lower.roll": 0.0,
                                          "body.head.pitch": 0.0}},
        {"time": 1 * delta_t, "data": {"body.arms.left.upper.pitch": -1.0,
                                        "body.arms.left.lower.roll": 0.1,
                                        "body.arms.right.upper.pitch": 0.0,
                                        "body.arms.right.lower.roll": 0.0,
                                        "body.head.pitch": 0.0}},
        {"time": 1.5 * delta_t, "data": {"body.arms.left.upper.pitch": -2.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": 0.0,
                                          "body.arms.right.lower.roll": 0.0,
                                          "body.head.pitch": 0.1}},
        {"time": 2 * delta_t, "data": {"body.arms.left.upper.pitch": -1.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": 0.0,
                                        "body.arms.right.lower.roll": 0.0,
                                        "body.head.pitch": 0.1}},
        {"time": 2.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": 0.0,
                                          "body.arms.right.lower.roll": 0.0,
                                          "body.head.pitch": 0.11}},
        {"time": 3 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": 0.0,
                                        "body.arms.right.lower.roll": 0.0,
                                        "body.head.pitch": 0.0}}
    ]
    frames2 = [
        {"time": 0.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": 0.0,
                                          "body.arms.right.lower.roll": 0.0,
                                          "body.head.pitch": 0.0}},
        {"time": 1 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": 0.5,
                                        "body.arms.right.lower.roll": -0.3,
                                        "body.head.pitch": 0.0}},
        {"time": 1.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": -1.0,
                                          "body.arms.right.lower.roll": -0.8,
                                          "body.head.pitch": 0.0}},
        {"time": 2 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": -0.5,
                                        "body.arms.right.lower.roll": -0.2,
                                        "body.head.pitch": 0.0}},
        {"time": 2.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": 0.0,
                                          "body.arms.right.lower.roll": 0.0,
                                          "body.head.pitch": 0.0}},
        {"time": 3 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": 0.0,
                                        "body.arms.right.lower.roll": 0.0,
                                        "body.head.pitch": 0.0}}
    ]
    frames3 = [
        {"time": 0.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": 0.0,
                                          "body.arms.right.lower.roll": 0.0,
                                          "body.head.pitch": 0.0}},
        {"time": 1 * delta_t, "data": {"body.arms.left.upper.pitch": -0.5,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": -0.5,
                                        "body.arms.right.lower.roll": 0.0,
                                        "body.head.pitch": -0.5}},
        {"time": 1.5 * delta_t, "data": {"body.arms.left.upper.pitch": -0.7,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": -0.7,
                                          "body.arms.right.lower.roll": 0.0,
                                          "body.head.pitch": -0.7}},
        {"time": 2 * delta_t, "data": {"body.arms.left.upper.pitch": -0.5,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": -0.5,
                                        "body.arms.right.lower.roll": 0.0,
                                        "body.head.pitch": -0.5}},
        {"time": 2.5 * delta_t, "data": {"body.arms.left.upper.pitch": -0.5,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": -0.5,
                                          "body.arms.right.lower.roll": 0.0,
                                          "body.head.pitch": -0.5}},
        {"time": 3 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": 0.0,
                                        "body.arms.right.lower.roll": 0.0,
                                        "body.head.pitch": 0.0}}
    ]
    framespreend = [
        {"time": 0.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": 0.0,
                                          "body.arms.right.lower.roll": 0.0,
                                          "body.head.pitch": 0.0}},
        {"time": 1 * delta_t, "data": {"body.arms.left.upper.pitch": -1.0,
                                        "body.arms.left.lower.roll": 0.1,
                                        "body.arms.right.upper.pitch": -1.0,
                                        "body.arms.right.lower.roll": 0.1,
                                        "body.head.pitch": 1.0}},
        {"time": 1.5 * delta_t, "data": {"body.arms.left.upper.pitch": -2.0,
                                          "body.arms.left.lower.roll": 0.1,
                                          "body.arms.right.upper.pitch": -2.0,
                                          "body.arms.right.lower.roll": 0.1,
                                          "body.head.pitch": 1.0}},
        {"time": 2 * delta_t, "data": {"body.arms.left.upper.pitch": -2.5,
                                        "body.arms.left.lower.roll": 0.1,
                                        "body.arms.right.upper.pitch": -2.5,
                                        "body.arms.right.lower.roll": 0.1,
                                        "body.head.pitch": 1.0}},
        {"time": 4 * delta_t, "data": {"body.arms.left.upper.pitch": -2.5,
                                        "body.arms.left.lower.roll": 0.1,
                                        "body.arms.right.upper.pitch": -2.5,
                                        "body.arms.right.lower.roll": 0.1,
                                        "body.head.pitch": 1.0}},
        {"time": 5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": 0.0,
                                        "body.arms.right.lower.roll": 0.0,
                                        "body.head.pitch": 0.0}}
    ]
    framesend = [
        {"time": 0.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": 0.0,
                                          "body.arms.right.lower.roll": 0.0,
                                          "body.head.pitch": 0.0}},
        {"time": 1 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": -1.0,
                                        "body.arms.right.lower.roll": 0.1,
                                        "body.head.pitch": 1.0}},
        {"time": 1.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": -2.0,
                                          "body.arms.right.lower.roll": 0.1,
                                          "body.head.pitch": 1.0}},
        {"time": 2 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": -2.5,
                                        "body.arms.right.lower.roll": 0.1,
                                        "body.head.pitch": 1.0}},
        {"time": 2.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": -2.5,
                                          "body.arms.right.lower.roll": 0.1,
                                          "body.head.pitch": 1.0}},
        {"time": 3 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": -2.5,
                                        "body.arms.right.lower.roll": -1.0,
                                        "body.head.pitch": 1.0}},
        {"time": 3.5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                          "body.arms.left.lower.roll": 0.0,
                                          "body.arms.right.upper.pitch": -2.5,
                                          "body.arms.right.lower.roll": -0.5,
                                          "body.head.pitch": 1.0}},
        {"time": 4 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": -2.5,
                                        "body.arms.right.lower.roll": -1.0,
                                        "body.head.pitch": 1.0}},
        {"time": 5 * delta_t, "data": {"body.arms.left.upper.pitch": 0.0,
                                        "body.arms.left.lower.roll": 0.0,
                                        "body.arms.right.upper.pitch": 0.0,
                                        "body.arms.right.lower.roll": 0.0,
                                        "body.head.pitch": 0.0}}
    ]

    def get_random_frames():
        """Randomly selects and returns one of the default frame sets."""
        return random.choice([frames, frames2, frames3])

    print("Performing movement animation...")
    # Select frame set based on frame_type if provided.
    if frame_type == "preend":
        frames_to_use = framespreend
    elif frame_type == "end":
        frames_to_use = framesend
    else:
        frames_to_use = get_random_frames()

    yield perform_movement(session, frames=frames_to_use, force=True)
    yield sleep(0.5)  # Ensures the movement completes before speaking
    print(f"Speaking: {text}")
    yield session.call("rie.dialogue.say", text=text)

@inlineCallbacks
def STT_continuous(session):
    # Commanding the robot to stand up
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    # Retrieve and configure hearing sensor
    info = yield session.call("rom.sensor.hearing.info")
    print("Sensor Info:", info)
    yield session.call("rom.sensor.hearing.sensitivity", 1650)
    yield session.call("rie.dialogue.config.language", lang="en")
    print("Listening to audio")
    # Subscribe to the hearing stream once at start
    yield session.subscribe(audio_processor.listen_continues, "rom.sensor.hearing.stream")
    yield session.call("rom.sensor.hearing.stream")
    
    # Keyword-handling functions 
    @inlineCallbacks
    def handle_keywords(session, user_input):
        keywords = ["end", "finish", "play again", "restart", "and the game"]
        if any(keyword in user_input for keyword in keywords):
            end_prompt = (
                "Present the players with an option to stop the game or play again.\n"
                "Say that if the player wants to stop the game they have to say 'dance'.\n"
            )
            response = chat.send_message_stream(end_prompt)
            reply = "".join(chunk.text for chunk in response)
            yield say_animated(session, reply, frame_type="preend")
            print("Game restart prompt sent.")

    @inlineCallbacks
    def handle_keywords1(session, user_input):
        keywords1 = ["confirm the ending", "confirm", "dance"]
        if any(keyword in user_input for keyword in keywords1):
            final_prompt = "Say goodbye and wish them best."
            response = chat.send_message_stream(final_prompt)
            reply = "".join(chunk.text for chunk in response)
            yield say_animated(session, reply, frame_type="end")
            print("Game finished.")

    # Extra part for the final assignment:
    # Initial prompt for the game, instructing the AI to greet the user and explain the rules.
    initial_prompt = (
        "We will play a game in the chat. The first thing you have to do is to greet the user and tell them that we will play a game. "
        "You have to say: Welcome, player! Today, we’re going to play a game of Guess the Word. I will ask you questions, and you must respond with yes or no. Let’s begin! "
        "The game that is going to be played is 'guess the word'. This game implies that you will ask yes or no questions and you have to try to guess the word. "
        "It is important that you do not go over a limit of 3 sentences in a row. "
        "Try to use narrowing down to the object, but also ask questions that broaden the horizon a bit. "
        "The first question must be: Is it a living thing?"
    )
    response = chat.send_message_stream(initial_prompt)
    reply = "".join(chunk.text for chunk in response)
    yield say_animated(session, reply)
    print("Greeting and game explanation sent.")

    # Playing the greeting audio in Romaninan
    yield session.call("rom.actuator.audio.stream",
                       url="https://audio.jukehost.co.uk/SJlB1E1TVmosKhi3bsiyfb6Z3j6Fl4zo",
                       sync=False
                       )

    # Main loop for continuous speech processing
    while True:
        if not audio_processor.new_words:
            yield sleep(0.5)
            print("Waiting for speech input...")
        else:
            word_array = audio_processor.give_me_words()
            print("I'm processing the words")
            print(word_array[-3:])  
            if word_array:
                # Extract the detected text. If the last entry is a tuple, take its first element.
                last_item = word_array[-1]
                if isinstance(last_item, tuple):
                    user_input = str(last_item[0])
                else:
                    user_input = str(last_item)
                print("User said:", user_input)
                # Handling keywords for ending or restarting the game.
                if any(keyword in user_input for keyword in ["end", "finish", "play again", "restart", "and the game"]):
                    yield handle_keywords(session, user_input)
                if any(keyword in user_input for keyword in ["confirm the ending", "confirm", "dance"]):
                    yield handle_keywords1(session, user_input)
                # Sending the user's response to AI chat.
                response = chat.send_message_stream(user_input)
                reply = "".join(chunk.text for chunk in response)
                break
        # Process audio input for new words
        audio_processor.loop()

    @inlineCallbacks
    def subscribe_once_to_touch(audio_url):
        # Use a mutable container to capture state
        touched_once = [False]
        sub_holder = {}

        @inlineCallbacks
        def touched(frame):
            if touched_once[0]:
                return
            if ("body.head.front" in frame["data"] or
                    "body.head.middle" in frame["data"] or
                    "body.head.rear" in frame["data"]):
                touched_once[0] = True
                print("Head has been touched! Replaying audio.")
                yield session.call("rom.actuator.audio.stream",
                                   url=audio_url,
                                   sync=False)
                yield sub_holder["subscription"].unsubscribe()
        sub_holder["subscription"] = (yield session.subscribe(touched, "rom.sensor.touch.stream"))
        yield sleep(6)

 # The next question
    question1 = ("Do not appologise. Just ask: 'Can you find it indoors?'")
    response = chat.send_message_stream(question1)
    reply = "".join(chunk.text for chunk in response)
    yield say_animated(session, reply)
    print("Q1 sent.")

    # Play Q1 audio (Romanian version) and subscribe to a one-shot touch event.
    audio_url_q1 = "https://audio.jukehost.co.uk/JuCMMGb4JE1mI1dXmN4WIAYH12oiUXvy"
    yield session.call("rom.actuator.audio.stream", url=audio_url_q1, sync=False)
    yield subscribe_once_to_touch(audio_url_q1)

    # Main loop for continuous speech processing
    while True:
        if not audio_processor.new_words:
            yield sleep(0.5)
            print("Waiting for speech input...")
        else:
            word_array = audio_processor.give_me_words()
            print("I'm processing the words")
            print(word_array[-3:])  # Print the last 3 sentences
            if word_array:
                # Extract the detected text. If the last entry is a tuple, take its first element.
                last_item = word_array[-1]
                if isinstance(last_item, tuple):
                    user_input = str(last_item[0])
                else:
                    user_input = str(last_item)
                print("User said:", user_input)
                if any(keyword in user_input for keyword in ["end", "finish", "play again", "restart", "and the game"]):
                    yield handle_keywords(session, user_input)
                if any(keyword in user_input for keyword in ["confirm the ending", "confirm", "dance"]):
                    yield handle_keywords1(session, user_input)
                response = chat.send_message_stream(user_input)
                reply = "".join(chunk.text for chunk in response)
                break
        # Process audio input for new words
        audio_processor.loop()

 # next question
    question2 = ("ask: 'Is it bigger than a car?'")
    response = chat.send_message_stream(question2)
    reply = "".join(chunk.text for chunk in response)
    yield say_animated(session, reply)
    print("Q2 sent.")

    # Play Q2 audio (Romanian version) and subscribe to a one-shot touch event.
    audio_url_q2 = "https://audio.jukehost.co.uk/EqegdooeH3CM4lMdK9EC9tuQssxahxIN"
    yield session.call("rom.actuator.audio.stream", url=audio_url_q2, sync=False)
    yield subscribe_once_to_touch(audio_url_q2)

    # Main loop for continuous speech processing
    while True:
        if not audio_processor.new_words:
            yield sleep(0.5)
            print("Waiting for speech input...")
        else:
            word_array = audio_processor.give_me_words()
            print("I'm processing the words")
            print(word_array[-3:])  
            if word_array:
                # Extract the detected text. If the last entry is a tuple, take its first element.
                last_item = word_array[-1]
                if isinstance(last_item, tuple):
                    user_input = str(last_item[0])
                else:
                    user_input = str(last_item)
                print("User said:", user_input)
                if any(keyword in user_input for keyword in ["end", "finish", "play again", "restart", "and the game"]):
                    yield handle_keywords(session, user_input)
                if any(keyword in user_input for keyword in ["confirm the ending", "confirm", "dance"]):
                    yield handle_keywords1(session, user_input)
                response = chat.send_message_stream(user_input)
                reply = "".join(chunk.text for chunk in response)
                break
            audio_processor.loop()
        # Process audio input for new words
        audio_processor.loop()

 # next question
    question3 = ("ask: 'Is it something you can eat?'")
    response = chat.send_message_stream(question3)
    reply = "".join(chunk.text for chunk in response)
    yield say_animated(session, reply)
    print("Q3 sent.")

    # Play Q3 audio (Romanian version) and subscribe to a one-shot touch event.
    audio_url_q3 = "https://audio.jukehost.co.uk/W4CqL5Yqj36OMxSzaqOvdvLFlyCUWNex"
    yield session.call("rom.actuator.audio.stream", url=audio_url_q3, sync=False)
    yield subscribe_once_to_touch(audio_url_q3)

    # Main loop for continuous speech processing
    while True:
        if not audio_processor.new_words:
            yield sleep(0.5)
            print("Waiting for speech input...")
        else:
            word_array = audio_processor.give_me_words()
            print("I'm processing the words")
            print(word_array[-3:])  
            if word_array:
                # Extract the detected text. If the last entry is a tuple, take its first element.
                last_item = word_array[-1]
                if isinstance(last_item, tuple):
                    user_input = str(last_item[0])
                else:
                    user_input = str(last_item)
                print("User said:", user_input)
                if any(keyword in user_input for keyword in ["end", "finish", "play again", "restart", "and the game"]):
                    yield handle_keywords(session, user_input)
                if any(keyword in user_input for keyword in ["confirm the ending", "confirm", "dance"]):
                    yield handle_keywords1(session, user_input)
                response = chat.send_message_stream(user_input)
                reply = "".join(chunk.text for chunk in response)
                break
        # Process audio input for new words
        audio_processor.loop()

 # next question
    question4 = ("ask: 'Is it used every day?'")
    response = chat.send_message_stream(question4)
    reply = "".join(chunk.text for chunk in response)
    yield say_animated(session, reply)
    print("Q3 sent.")

    # Play Q4 audio (Romanian version) and subscribe to a one-shot touch event.
    audio_url_q4 = "https://audio.jukehost.co.uk/TvkVGtB5VGa7azhrZdCcXFzw5mOpjFzc"
    yield session.call("rom.actuator.audio.stream", url=audio_url_q4, sync=False)
    yield subscribe_once_to_touch(audio_url_q4)

    # Main loop for continuous speech processing
    while True:
        if not audio_processor.new_words:
            yield sleep(0.5)
            print("Waiting for speech input...")
        else:
            word_array = audio_processor.give_me_words()
            print("I'm processing the words")
            print(word_array[-3:])  
            if word_array:
                # Extract the detected text. If the last entry is a tuple, take its first element.
                last_item = word_array[-1]
                if isinstance(last_item, tuple):
                    user_input = str(last_item[0])
                else:
                    user_input = str(last_item)
                print("User said:", user_input)
                if any(keyword in user_input for keyword in ["end", "finish", "play again", "restart", "and the game"]):
                    yield handle_keywords(session, user_input)
                    continue
                if any(keyword in user_input for keyword in ["confirm the ending", "confirm", "dance"]):
                    yield handle_keywords1(session, user_input)
                    break
                response = chat.send_message_stream(user_input)
                reply = "".join(chunk.text for chunk in response)
                print("Gemini's Response:", reply)
                yield say_animated(session, reply)
                yield sleep(0.5)
        # Process audio input for new words
        audio_processor.loop()

@inlineCallbacks
def main(session, details):
    """Main function that starts all processes."""
    output_dir = "output"
    output_file = os.path.join(output_dir, "output.wav")
    os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(output_file):
        with open(output_file, "wb") as f:
            f.write(b"")
    print("Starting main function...")
    # Get initial proprioceptive data
    frames = yield session.call("rom.sensor.proprio.read")
    print("Current engine status:")
    print(frames[0]["data"])
    # Subscribe to proprioceptive stream
    yield session.subscribe(proprio, "rom.sensor.proprio.stream")
    yield session.call("rom.sensor.proprio.stream")
    yield session.call("rom.optional.behavior.play", name="BlocklyStand")
    # Face recognition imprementation
    yield session.call("rie.vision.face.find")
    yield session.call("rie.dialogue.say", text="I found you!")
    yield session.call("rom.sensor.touch.stream")
    yield sleep(2)

    # Start continuous speech-to-text processing
    yield STT_continuous(session)
    session.leave()  # End the session when done

# WAMP component setup
wamp = Component(
    transports=[{"url": "ws://wamp.robotsindeklas.nl", "serializers": ["msgpack"], "max_retries": 0}],
    realm="rie.67e275a1540602623a34e826",
)

wamp.on_join(main)  # Register main function when WAMP session starts

if __name__ == "__main__":
    run([wamp])
