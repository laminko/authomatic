from google.appengine.api import users
from authomatic import providers
from authomatic.exceptions import FailureError
import logging
import authomatic.core as core

class GAEOpenID(providers.AuthenticationProvider):
    """OpenID provider based on google.appengine.api.users library."""
    
    @providers._login_decorator
    def login(self):
        """
        Launches the OpenID authentication procedure.
        
        Accepts oi_identifier optional parameter
        """
        
        if self.identifier:
            self._log(logging.INFO, 'Starting OpenID authentication procedure.')
            
            url = users.create_login_url(dest_url=self.adapter.url, federated_identity=self.identifier)
            
            self._log(logging.INFO, 'Redirecting user to {}.'.format(url))
            
            self.adapter.redirect(url)
        else:
            # returned from redirect or somebody requested without identifier
            self._log(logging.INFO, 'Continuing OpenID authentication procedure after redirect.')
            
            user = users.get_current_user()
            if user:
                self._log(logging.INFO, 'Authentication successful.')
                self._log(logging.INFO, 'Creating user.')
                self.user = core.User(self,
                                     user_id=user.federated_identity(),
                                     email=user.email(),
                                     gae_user=user)
                # We're done
            else:
                raise FailureError('Unable to authenticate user id!')

class Yahoo(GAEOpenID):
    identifier = 'me.yahoo.com'

class Google(GAEOpenID):
    identifier = 'https://www.google.com/accounts/o8/id'