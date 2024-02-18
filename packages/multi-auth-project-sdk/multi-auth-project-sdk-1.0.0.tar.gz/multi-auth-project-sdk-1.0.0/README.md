
# Getting Started with MultiAuth-Sample

## Introduction

API for Markdown Notes app.

## Install the Package

The package is compatible with Python versions `3 >=3.7, <= 3.11`.
Install the package from PyPi using the following pip command:

```python
pip install multi-auth-project-sdk==1.0.0
```

You can also view the package at:
https://pypi.python.org/pypi/multi-auth-project-sdk/1.0.0

## Test the SDK

You can test the generated SDK and the server with test cases. `unittest` is used as the testing framework and `pytest` is used as the test runner. You can run the tests as follows:

Navigate to the root directory of the SDK and run the following commands

```
pip install -r test-requirements.txt
pytest
```

## Initialize the API Client

**_Note:_** Documentation for the client can be found [here.](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/client.md)

The following parameters are configurable for the API Client:

| Parameter | Type | Description |
|  --- | --- | --- |
| `access_token` | `str` |  |
| `port` | `str` | *Default*: `'80'` |
| `suites` | `SuiteCodeEnum` | *Default*: `1` |
| `environment` | Environment | The API environment. <br> **Default: `Environment.TESTING`** |
| `http_client_instance` | `HttpClient` | The Http Client passed from the sdk user for making requests |
| `override_http_client_configuration` | `bool` | The value which determines to override properties of the passed Http Client from the sdk user |
| `http_call_back` | `HttpCallBack` | The callback value that is invoked before and after an HTTP call is made to an endpoint |
| `timeout` | `float` | The value to use for connection timeout. <br> **Default: 60** |
| `max_retries` | `int` | The number of times to retry an endpoint call if it fails. <br> **Default: 0** |
| `backoff_factor` | `float` | A backoff factor to apply between attempts after the second try. <br> **Default: 2** |
| `retry_statuses` | `Array of int` | The http statuses on which retry is to be done. <br> **Default: [408, 413, 429, 500, 502, 503, 504, 521, 522, 524]** |
| `retry_methods` | `Array of string` | The http methods on which retry is to be done. <br> **Default: ['GET', 'PUT']** |
| `basic_auth_credentials` | [`BasicAuthCredentials`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/basic-authentication.md) | The credential object for Basic Authentication |
| `api_key_credentials` | [`ApiKeyCredentials`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/custom-query-parameter.md) | The credential object for Custom Query Parameter |
| `api_header_credentials` | [`ApiHeaderCredentials`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/custom-header-signature.md) | The credential object for Custom Header Signature |
| `o_auth_ccg_credentials` | [`OAuthCCGCredentials`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/oauth-2-client-credentials-grant.md) | The credential object for OAuth 2 Client Credentials Grant |
| `o_auth_acg_credentials` | [`OAuthACGCredentials`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/oauth-2-authorization-code-grant.md) | The credential object for OAuth 2 Authorization Code Grant |
| `o_auth_ropcg_credentials` | [`OAuthROPCGCredentials`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/oauth-2-resource-owner-credentials-grant.md) | The credential object for OAuth 2 Resource Owner Credentials Grant |
| `o_auth_bearer_token_credentials` | [`OAuthBearerTokenCredentials`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/oauth-2-bearer-token.md) | The credential object for OAuth 2 Bearer token |

The API client can be initialized as follows:

```python
client = MultiauthsampleClient(
    access_token='accessToken',
    basic_auth_credentials=BasicAuthCredentials(
        username='Username',
        password='Password'
    ),
    api_key_credentials=ApiKeyCredentials(
        token='token',
        api_key='api-key'
    ),
    api_header_credentials=ApiHeaderCredentials(
        token='token',
        api_key='api-key'
    ),
    o_auth_ccg_credentials=OAuthCCGCredentials(
        o_auth_client_id='OAuthClientId',
        o_auth_client_secret='OAuthClientSecret'
    ),
    o_auth_acg_credentials=OAuthACGCredentials(
        o_auth_client_id='OAuthClientId',
        o_auth_client_secret='OAuthClientSecret',
        o_auth_redirect_uri='OAuthRedirectUri',
        o_auth_scopes=[
            OAuthScopeOAuthACGEnum.READ_SCOPE
        ]
    ),
    o_auth_ropcg_credentials=OAuthROPCGCredentials(
        o_auth_client_id='OAuthClientId',
        o_auth_client_secret='OAuthClientSecret',
        o_auth_username='OAuthUsername',
        o_auth_password='OAuthPassword'
    ),
    o_auth_bearer_token_credentials=OAuthBearerTokenCredentials(
        access_token='AccessToken'
    )
)
```

## Environments

The SDK can be configured to use a different environment for making API calls. Available environments are:

### Fields

| Name | Description |
|  --- | --- |
| production | - |
| testing | **Default** |

## Authorization

This API uses the following authentication schemes.

* [`basicAuth (Basic Authentication)`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/basic-authentication.md)
* [`apiKey (Custom Query Parameter)`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/custom-query-parameter.md)
* [`apiHeader (Custom Header Signature)`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/custom-header-signature.md)
* [`OAuthCCG (OAuth 2 Client Credentials Grant)`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/oauth-2-client-credentials-grant.md)
* [`OAuthACG (OAuth 2 Authorization Code Grant)`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/oauth-2-authorization-code-grant.md)
* [`OAuthROPCG (OAuth 2 Resource Owner Credentials Grant)`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/oauth-2-resource-owner-credentials-grant.md)
* [`OAuthBearerToken (OAuth 2 Bearer token)`](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/$a/https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/oauth-2-bearer-token.md)
* `CustomAuth (Custom Authentication)`

## List of APIs

* [O Auth Authorization](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/controllers/o-auth-authorization.md)
* [Authentication](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/controllers/authentication.md)

## Classes Documentation

* [Utility Classes](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/utility-classes.md)
* [HttpResponse](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/http-response.md)
* [HttpRequest](https://www.github.com/Syed-Subtain/multi-auth-project-python-sdk/tree/1.0.0/doc/http-request.md)

