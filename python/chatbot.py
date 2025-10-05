# Import the necessary libraries.
import random
import re



class CryptoChatbot:
    def __init__(self):
        # Possible answers of chatbot.
        self.responses = {
            "greetings": [
                "Γεια σου! Πως μπορώ να σε βοηθήσω σήμερα;",
                
                "Καλώς ήρθες! Σε τι θα μπορούσα να σου φανώ χρήσιμος;"
            ],
            "price": [
                "Μπορείς να δεις την τιμή ενός κρυπτονομίσματος επιλέγοντας το από την λίστα.",
                "Πες μου σε ποιο κρυπτονόμισμα θα ήθελες να μάθεις ποια είναι η τιμή του."
            ],
            "buy": [
                "Δεν παρέχονται συμβουλές αγοράς. Καλύτερα να κάνεις την δική σου έρευνα..",
                "Για συμβουλές κάποιας επενδυτικής κίνησης, συμβουλεύσου έναν ειδικό."
            ],
            "best": [
                "Το 'καλύτερο' κρυπτονόμισμα εξαρτάται από τα κριτήρια σου.",
                "Κοίταξε την κεφαλοποίηση αγοράς για να δεις τα κορυφαία νομίσματα."
            ],
            "cap": [
                "Μπορείς να δεις την κεφαλοποίηση κάθε νομίσματος στον πίνακα δεδομένων.",
                "Η κεφαλοποίση αγοράς υπολογίζεται ως: (Τιμή) x (Συνολική Προσφορά)."
            ],
            "volatility": [
                "Οι μεγάλες μεταβολές τιμών αποτελούν συχνές στον χώρο των κρυπτονομισμάτων.",
                "Η μεταβολή της τιμής ενός κρυπτονομίσματος επηρεάζεται από την κεφαλοποίηση αγοράς του."
            ],
            "safety": [
                "Χρησιμοποίησε πάντα αξιόπιστες πλατφόρμες και κράτα τα κρυπτονομίσματα σου σε cold wallet για ασφάλεια.",
                "Η ασφάλεια εξαρτάται απο τις πρακτικές αποθήκευσης και συναλλαγών σου."
            ],
            "future": [
                "Κανείς όπως και εγώ δεν μπορούμε να προβλέψουμε το μέλλον των κρυπτονομισμάτων με σιγουριά.",
                "Οι προβλέψεις ποικίλλουν. Κάποιοι πιστεύουν σε μεγάλη άνοδο και άλλοι σε πτώση."
            ],
            "altcoins": [
                "Τα altcoins είναι όλα εκείνα τα κρυπτονομίσματα εκτός από το Bitcoin. Κάποια δημοφιλή από αυτά είναι το Ethereum, Solana, Cardano κλπ.",
                "Κάποια altcoins βρίσκονται στον πίνακα, όπου μπόρεις να ανατρέξεις για να μάθεις περισσότερες πληροφορίες για το καθένα."
            ],
            "thanks": [
                "Παρακαλώ! Χαίρομαι που μπόρεσα να σε βοηθήσω.",
                "Ήταν χαρά μου που σε βοήθησα! Αν έχεις άλλες απορίες, μην διστάσεις να με ρωτήσεις!"
            ],
            "default": [
                "Δεν κατάλαβα. Μπορείς να με ρωτήσεις κάτι άλλο;",
                "Δεν έχω απάντηση για αυτό. Ρώτα με κάτι σχετικό με τα κρυπτονομίσματα."
            ],
        }

        # Keywords that helps chatbot answer to user.
        self.keywords = {
            "greetings": ["γεια σου", "hello", "χαίρετε", "καλημέρα", "καλησπέρα"],
            "price": ["τιμή", "price", "πόσο κοστίζει", "value"],
            "buy": ["αγορά", "buy", "αξίζει", "invest", "επένδυση"],
            "best": ["καλύτερο", "top", "κορυφαίο", "υψηλότερο σε", "best"],
            "cap": ["market cap", "capitalization", "κεφαλοποίηση"],
            "volatility": ["αστάθεια", "μεταβλητότητα", "volatility"],
            "safety": ["safe", "wallet", "πορτοφολι", "ασφάλεια", "ασφαλές"],
            "future": ["μέλλον", "πρόβλεψη", "future", "prediction"],
            "altcoins": ["altcoin", "altcoins", "αλτκοιν"],
            "thanks": ["ευχαριστώ", "thanks", "thank you"]
        }




    def get_response(self, user_input):
        user_input = user_input.lower()


        for words, keys in self.keywords.items():
            for key in keys:
                if key in user_input:
                    return random.choice(self.responses[words])


        return random.choice(self.responses["default"])


    
    # User begins communication with the chatbot
    def start_chat(self):
        print("\nΤο Bitbot είναι στην διάθεση σου (Γράψτε 'exit' για έξοδο) ===")
        print(random.choice(self.responses["greetings"]))

        # As long as user don't give inputs with the keyword 'exit', then chatbot keeps give responses.
        while True:
            user_input = input("\nYou: ")

            if user_input != "exit":
                response = self.get_response(user_input)
                print(f"Bitbot: {response}")
            else:
                print("Bitbot: Καλή συνέχεια! Ελπίζω να βοήθησα.")
                break