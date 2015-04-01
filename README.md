JSAutoLogin
===========

JavaScript library for single sign-on


What is does
------------

This JavaScript library is way to implement Single Signon
with protocols that were never meant to do this, like OpenID
or SAML for web applications.


How it does this
----------------

This library consists of two different parts: one of them
is used in the user-visible page and tries to log the user
in in the background.

To do this, it will load the page specified in the `login_url`
argument to  the `tryBackgroundLogin` function in a hidden
iFrame.
After that, it will listen for any response messages from
inside the hidden iFrame, after which it will call either the
`callback_success` or `callback_failed` callback with the
results (note that `callback_failed` is optional).
In the `callback_success`, the page should update the DOM
to indicate to the user he/she has been logged in.

Note:
Because the login_url is loaded in a hidden iFrame, it should
not display a user interface at any time. If you are using
OpenID, this can be indicated to the OpenID provider by using
the checkid_immediate mode (called "immediate mode" in many
libraries).


The second part of the library is the page that returns the
login result (success or failure) back to the user-visible
page, as noted before, this is a page that's not visible
to the user, but only sends back a message to the
`tryBackgroundLogin` call.


API
---

This library consists of two functions, that correspond
one-to-one with the previously mentioned steps:
`tryBackgroundLogin`(`login_url`, `callback_success`, `callback_failed`)
  This is the function that's used in the user-visible page
  to kick of the process of the background login process.
  `login_url`: (REQUIRED) The url of the applications login
    page, which should never show a UI, but should at some
    point call `respondToLogin`.
  `callback_success`: (REQUIRED) A callback function that will
    be called once the login completed successfully. This function
    should take a single argument: the data object passed on from
    the login response page.
  `callback_failed`: (OPTIONAL) A callback function that will
    be called when the login response page returns an error message
    based on the login response. This function should take a single
    argument: the data object passed on from the login response page.

`respondToLogin`(`targetOrigin`, `success`, `data`)
  This is the function that's called in the login response page
  to return the login result back to the user-visible page.
  `targetOrigin`: (REQUIRED) The scheme-hostname-port combination
    that the application is running on. This is used to prevent
    user information from leaving the application. If the scheme,
    hostname or port specified in this argument do not match the
    values from the page calling the background login, the response
    message will be ignored by the browser. For testing purposes,
    this security function can be disabled by setting to '*'.
    WARNING: DO SET THIS IN PRODUCTION!
    Example: 'http://myapp.example.com:8080'.
  `success`: (REQUIRED) A boolean whether or not login was successful.
  `data`: (OPTIONAL) Any data you want to send to the user-visible page.
    This could for example include the username so the user-visible page
    can update the DOM to indicate the username.


Example
-------

For an example application, written in Python and using the Flask
framework, that uses this library, please check the "Example"
directory.


License
-------

The JSAutoLogin library itself is licensed under the GPLv3, or
(at your at your option) any later version.
The Example code is licensed under the CC0.
