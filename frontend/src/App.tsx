import { MantineProvider } from '@mantine/core'
import { theme } from './theme'
import { Router } from './Router';
import '@mantine/core/styles.layer.css';

import "vanilla-cookieconsent/dist/cookieconsent.css";
import * as CookieConsent from "vanilla-cookieconsent";
import { useEffect } from 'react';

function App() {

  useEffect(() => {
    CookieConsent.run({
      guiOptions: {
        consentModal: {
          layout: 'box',
          position: 'bottom right',
          equalWeightButtons: true,
          flipButtons: false,
        },
        preferencesModal: {
          layout: 'box',
          position: 'left',
          equalWeightButtons: true,
          flipButtons: false,
        },
      },

      onFirstConsent: function () {
        console.log('onFirstAction fired');
        if (CookieConsent.acceptedCategory('analytics')) {
          var script = document.createElement('script')
          script.setAttribute("className", "sleekplan_script")
          script.type = "text/javascript"
          script.text = String.raw`window.$sleek=[];window.SLEEK_PRODUCT_ID=490237571;(function(){d=document;s=d.createElement("script");s.src="https://client.sleekplan.com/sdk/e.js";s.async=1;d.getElementsByTagName("head")[0].appendChild(s);})();`
          document.head.appendChild(script);
        } else {

        }
      },

      onConsent: function ({ }) {  // cookie
        console.log('onConsent fired ...');
        if (CookieConsent.acceptedCategory('analytics')) {
          if (document.querySelector('script[src="https://client.sleekplan.com/sdk/e.js"]')) {
            console.log('sleekplan found')
          } else {
            console.log('sleekplan not found, adding script')
            var script = document.createElement('script')
            script.setAttribute("className", "sleekplan_script")
            script.type = "text/javascript"
            script.text = String.raw`window.$sleek=[];window.SLEEK_PRODUCT_ID=490237571;(function(){d=document;s=d.createElement("script");s.src="https://client.sleekplan.com/sdk/e.js";s.async=1;d.getElementsByTagName("head")[0].appendChild(s);})();`
            document.head.appendChild(script);
          }
        }
      },

      onChange: function ({ }) { //cookie, changedCategories, changedServices
        console.log('onChange fired ...');
        if (CookieConsent.acceptedCategory('analytics')) {
          if (document.querySelector('script[src="https://client.sleekplan.com/sdk/e.js"]')) {
            console.log('sleekplan found')
          } else {
            console.log('sleekplan not found, adding script')
            var script = document.createElement('script')
            script.setAttribute("className", "sleekplan_script")
            script.type = "text/javascript"
            script.text = String.raw`window.$sleek=[];window.SLEEK_PRODUCT_ID=490237571;(function(){d=document;s=d.createElement("script");s.src="https://client.sleekplan.com/sdk/e.js";s.async=1;d.getElementsByTagName("head")[0].appendChild(s);})();`
            document.head.appendChild(script);
          }
        } else {
          document.querySelector('script[src="https://client.sleekplan.com/sdk/e.js"]')?.remove()
          document.querySelectorAll(".sleekplan_script").forEach(el => el.remove());
          window.location.reload()
        }
      },

      categories: {
        necessary: {
          readOnly: true,
          enabled: true,
        },
        analytics: {
          autoClear: {
            cookies: [
              {
                name: /^(_ga|_gid)/,
              },
              {
                name: /^_gcl/,
              },
              {
                name: /^_sleek/, // remove all _sleek cookies from sleekplan
              },
              {
                name: /^intercom/,
              },
              {
                name: /^partnero/
              },
              {
                name: /^ph_phc/,
              },
            ],
          },
        },
      },

      language: {
        default: 'en',

        translations: {
          en: {
            consentModal: {
              title: "We value your privacy",
              description:
                'Our website uses minimal cookies solely to allow you to provide feedback. These cookies will be enabled only if you accept explicitly. <a href="#privacy-policy" data-cc="show-preferencesModal" class="cc__link">Manage preferences</a>',
              acceptAllBtn: 'Accept all',
              acceptNecessaryBtn: 'Reject all',
              showPreferencesBtn: 'Manage preferences',
              //closeIconLabel: 'Close',
              footer: `
                <a href="/privacy#privacy-policy">Privacy Policy</a>
              `,
            },
            preferencesModal: {
              title: 'Cookie preferences',
              acceptAllBtn: 'Accept all',
              acceptNecessaryBtn: 'Reject all',
              savePreferencesBtn: 'Save preferences',
              closeIconLabel: 'Close',
              sections: [
                {
                  title: 'Cookie Usage',
                  description:
                    'We use cookies minimally to ensure the basic functionalities of the website and to allow you to share your feedback with us. You can choose for each category to opt-in/out whenever you want. For more details relative to cookies and other sensitive data, please read the full <a href="#" class="cc__link">privacy policy</a>.',
                },
                {
                  title: 'Strictly necessary cookies',
                  description: 'These are the cookies that are necessary for the Shelf Help to function properly',
                  linkedCategory: 'necessary',
                },
                {
                  title: 'Feedback and Analytics cookies',
                  description: 'These cookies are used if you want to provide optional feedback about the application. We do not directly use Google Analytics, but Sleekplan does, so if you want to give us feedback and see upcoming changes, accept these cookies.',
                  linkedCategory: 'analytics',
                  cookieTable: {
                    caption: 'Cookie table',
                    headers: {
                      name: 'Cookie',
                      domain: 'Domain',
                      desc: 'Description'
                    },
                    body: [
                      {
                        name: '_ga',
                        domain: ".sleekplan.com",
                        desc: 'Google Analytics introduced by Sleekplan for basic analytics',
                      },
                      {
                        name: '_gcl_au',
                        domain: location.hostname,
                        desc: 'Google Analytics introduced by Sleekplan for advertising',
                      },
                      {
                        name: '_sleek_product',
                        domain: '.sleekplan.com',
                        desc: 'Sleekplan information for logged in users and session data'
                      },
                      {
                        name: '_sleek_session',
                        domain: '.sleekplan.com',
                        desc: 'Sleekplan session information for the optional sleekplan widget'
                      },
                      {
                        name: '_sleek_storage',
                        domain: '.sleekplan.com',
                        desc: 'Session data for announcements/pop-ups for optional sleekplan widget'
                      },
                      {
                        name: 'intercom-session',
                        domain: '.sleekplan.com',
                        desc: 'Sleekplan integration with intercom for customer support'
                      },
                      {
                        name: 'intercom-device-id',
                        domain: '.sleekplan.com',
                        desc: 'Sleekplan integration with intercom for customer support'
                      },
                      {
                        name: 'partnero-session-uuid',
                        domain: '.sleekplan.com',
                        desc: 'Sleekplan dependency'
                      },
                      {
                        name: 'ph_phc',
                        domain: '.sleekplan.com',
                        desc: 'Posthog analytics introduced by Sleekplan'
                      }
                    ]
                  },
                },
                {
                  title: 'More information',
                  description:
                    'For any queries in relation to my policy on cookies and your choices, please email shelfhelpappdev@gmail.com.',
                },
              ],
            },
          },
        },
      },
    });
  }, []);

  return (
    <MantineProvider theme={theme} >
      <Router />
    </MantineProvider>
  )
}

export default App
