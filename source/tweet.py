import private_credentials
import tweepy


def send(text):
   auth = tweepy.OAuthHandler(private_credentials.consumer_key, private_credentials.consumer_secret)
   auth.set_access_token(private_credentials.access_token, private_credentials.access_token_secret)
   api = tweepy.API(auth)

   text = text[:280]
   api.update_status(status=text)