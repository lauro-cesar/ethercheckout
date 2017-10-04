SESSION_KEY = "BDC384F4-B553-4108-90E3-55D4F5EB44EC-3049ACEA-1D83-4B00-BA76-3A33ED43DD18-F94F5A79-81CF-47EB-9C42-4F227DBF4491-3C876AA0-A2BF-429E-9EAD-0083F41E9DB5"

AMAZON_ACCESS_KEY="AKIAJNV3URTMY6USU2IA"
AMAZON_SECRET_KEY="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"
AMAZON_ASSOCIATE_TAG="ethercheckout-20"


GOOGLE_APP_ID = '904943486754-vrb375kdkmqb8gjv01jke4633gteg88c.apps.googleusercontent.com'
GOOGLE_APP_SECRET = 'U0Ib1CryE_-EfGkQsuSJMiGe'

# Facebook auth apis
FACEBOOK_APP_ID = 'app id'
FACEBOOK_APP_SECRET = 'app secret'

# Key/secret for both LinkedIn OAuth 1.0a and OAuth 2.0
# https://www.linkedin.com/secure/developer
LINKEDIN_KEY = 'consumer key / client id'
LINKEDIN_SECRET = 'consumer secret / client secret'

# https://manage.dev.live.com/AddApplication.aspx
# https://manage.dev.live.com/Applications/Index
WL_CLIENT_ID = 'client id'
WL_CLIENT_SECRET = 'client secret'

# https://dev.twitter.com/apps
TWITTER_CONSUMER_KEY = 'oauth1.0a consumer key'
TWITTER_CONSUMER_SECRET = 'oauth1.0a consumer secret'

# https://foursquare.com/developers/apps
FOURSQUARE_CLIENT_ID = 'client id'
FOURSQUARE_CLIENT_SECRET = 'client secret'

# config that summarizes the above
AUTH_CONFIG = {
  # OAuth 2.0 providers
  'google': (GOOGLE_APP_ID, GOOGLE_APP_SECRET,
             'https://www.googleapis.com/auth/userinfo.profile'),
  'googleplus': (GOOGLE_APP_ID, GOOGLE_APP_SECRET, 'profile'),
  'linkedin2': (LINKEDIN_KEY, LINKEDIN_SECRET, 'r_basicprofile'),
  'facebook': (FACEBOOK_APP_ID, FACEBOOK_APP_SECRET, 'user_about_me'),
  'windows_live': (WL_CLIENT_ID, WL_CLIENT_SECRET, 'wl.signin'),
  'foursquare': (FOURSQUARE_CLIENT_ID, FOURSQUARE_CLIENT_SECRET,
                 'authorization_code'),

  # OAuth 1.0 providers don't have scopes
  'twitter': (TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET),
  'linkedin': (LINKEDIN_KEY, LINKEDIN_SECRET),

  # OpenID doesn't need any key/secret
}

AUTH_OPTIONAL_PARAMS = {
  #	Provider auth init optional parameters
  # '<provider>': {'<parameter_name>': '<value>'}
  # ex. 'twitter' : {'force_login': True}
}