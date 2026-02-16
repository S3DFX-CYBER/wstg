# API टेस्टिंग

वेब APIs बहुत लोकप्रिय हो गए हैं क्योंकि ये दूसरे प्रोग्राम्स को वेबसाइटों से आसानी से जुड़ने देते हैं। इस गाइड में हम APIs के बारे में बुनियादी बातें और उनकी सुरक्षा कैसे टेस्ट करें, यह सीखेंगे।

## मूल अवधारणाएं

REST (Representational State Transfer) एक तरीका है जिससे डेवलपर APIs बनाते हैं।
REST स्टाइल में बनी Web APIs को REST API कहते हैं।
REST APIs संसाधनों (resources) तक पहुंचने के लिए URIs (Uniform Resource Identifiers) का उपयोग करती हैं। [RFC3986](https://tools.ietf.org/html/rfc3986) के अनुसार URI की बनावट इस प्रकार होती है:

> URI = scheme "://" authority "/" path [ "?" query ] [ "#" fragment ]

हम URI के path में रुचि रखते हैं क्योंकि यह यूजर और संसाधनों के बीच संबंध दिखाता है।
उदाहरण: `https://api.test.xyz/admin/testing/report`, यह टेस्टिंग की रिपोर्ट दिखाता है, जिसमें एडमिन यूजर और उनकी रिपोर्ट के बीच संबंध है।

किसी भी URI का path REST API के resource model को दर्शाता है, resources को forward slash (/) से अलग किया जाता है और Top-Down डिज़ाइन पर आधारित होते हैं।
उदाहरण:

- `https://api.test.xyz/admin/testing/report`
- `https://api.test.xyz/admin/testing/`
- `https://api.test.xyz/admin/`

REST API requests [RFC7231](https://tools.ietf.org/html/rfc7231) में परिभाषित [HTTP Request Methods](https://tools.ietf.org/html/rfc7231#section-4) का पालन करते हैं:

| Methods | विवरण                                |
|---------|--------------------------------------|
| GET     | संसाधन की स्थिति प्राप्त करें        |
| POST    | नया संसाधन बनाएं                     |
| PUT     | संसाधन को अपडेट करें                 |
| DELETE  | संसाधन को हटाएं                      |
| HEAD    | संसाधन से जुड़ा metadata प्राप्त करें |
| OPTIONS | उपलब्ध methods की सूची दें          |

REST APIs क्लाइंट को उनके request के परिणाम के बारे में बताने के लिए HTTP response message के response status code का उपयोग करते हैं।

| Response Code | Response Message      | विवरण                                                                              |
|---------------|-----------------------|------------------------------------------------------------------------------------|
| 200           | OK                    | क्लाइंट के request को सफलतापूर्वक प्रोसेस किया गया                                 |
| 201           | Created               | नया संसाधन बनाया गया                                                               |
| 301           | Moved Permanently     | स्थायी रूप से redirect किया गया                                                    |
| 304           | Not Modified          | Caching से संबंधित response जब क्लाइंट के पास server जैसी ही copy हो            |
| 307           | Temporary Redirect    | संसाधन का अस्थायी redirection                                                      |
| 400           | Bad Request           | क्लाइंट द्वारा गलत request                                                         |
| 401           | Unauthorized          | क्लाइंट को request करने या किसी संसाधन तक पहुंचने की अनुमति नहीं है                |
| 402           | Forbidden             | क्लाइंट को संसाधन तक पहुंचने से रोका गया है                                        |
| 404           | Not Found             | संसाधन मौजूद नहीं है या request के आधार पर गलत है                                  |
| 405           | Method Not Allowed    | अमान्य method या अज्ञात method का उपयोग किया गया                                  |
| 500           | Internal Server Error | आंतरिक त्रुटि के कारण server request को प्रोसेस नहीं कर सका                       |

HTTP headers का उपयोग requests और responses में किया जाता है।
API requests करते समय, Content-Type header का उपयोग किया जाता है और इसे `application/json` पर सेट किया जाता है क्योंकि message body में JSON data format होता है।

Web authentication के प्रकार इन पर आधारित हैं:

- Bearer Tokens: `Authorization: Bearer <token>` header से पहचाने जाते हैं। एक बार यूजर लॉगिन करने के बाद, उन्हें एक bearer token दिया जाता है जो हर request पर भेजा जाता है ताकि यूजर को authenticate और authorize किया जा सके और OAuth 2.0 protected resources तक पहुंच मिल सके।
- HTTP Cookies: `Cookie: <name>=<unique value>` header से पहचाने जाते हैं। यूजर के सफल लॉगिन पर, server `Set-Cookie` header के साथ reply करता है जिसमें इसका नाम और unique value होती है। हर request पर, browser स्वचालित रूप से इसे उस server को जाने वाली requests में जोड़ देता है, [SOP](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy) का पालन करते हुए।
- Basic HTTP authentication: `Authorization: Basic <base64 value>` header से पहचाना जाता है। जब यूजर लॉगिन करने की कोशिश करता है, तो request उल्लिखित header के साथ भेजा जाता है जिसमें base64 value होती है, जिसकी सामग्री `username:password` होती है। यह authentication के सबसे कमजोर रूपों में से एक है क्योंकि यह हर request पर username और password को encoded रूप में transmit करता है, जिसे आसानी से retrieve किया जा सकता है।

## कैसे टेस्ट करें

### सामान्य टेस्टिंग विधि

Step 1: Endpoint की सूची बनाएं और अलग-अलग request method बनाएं: यूजर प्रोफाइल के साथ लॉगिन करें और इस role के endpoints की सूची बनाने के लिए spider tool का उपयोग करें।
Endpoints की जांच करने के लिए, आपको अलग-अलग request methods बनाने और देखने की जरूरत होगी कि API कैसे व्यवहार करता है।

Step 2: Bugs का फायदा उठाएं - जैसा कि step 1 में endpoints की सूची बनाना और HTTP methods के साथ endpoints की जांच करना सीखा, हम bug का फायदा उठाने के कुछ तरीके खोजेंगे। कुछ टेस्टिंग रणनीतियां नीचे दी गई हैं:

- IDOR testing
- Privilege escalation

### विशिष्ट टेस्टिंग – (Token-Based) Authentication

Token-based authentication हर HTTP request के साथ एक signed token (server द्वारा verified) भेजकर लागू किया जाता है।

सबसे अधिक उपयोग किया जाने वाला token format JSON Web Token (JWT) है, जो [RFC7519](https://tools.ietf.org/html/rfc7519) में परिभाषित है। [Testing JSON Web Tokens](/document/4-Web_Application_Security_Testing/06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md) गाइड में JWTs को कैसे टेस्ट करें इसके बारे में अधिक जानकारी है।

## संबंधित टेस्ट केस

- [IDOR](https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/05-Authorization_Testing/04-Testing_for_Insecure_Direct_Object_References.md)
- [Privilege escalation](https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/05-Authorization_Testing/03-Testing_for_Privilege_Escalation.md)
- सभी [Session Management](https://github.com/OWASP/wstg/tree/master/document/4-Web_Application_Security_Testing/06-Session_Management_Testing) test cases
- [Testing JSON Web Tokens](/document/4-Web_Application_Security_Testing/06-Session_Management_Testing/10-Testing_JSON_Web_Tokens.md)

## टूल्स

- ZAP
- Burp suite

## संदर्भ

- [REST HTTP Methods](https://restfulapi.net/http-methods/)
- [RFC3986 URI](https://tools.ietf.org/html/rfc3986)
- [JWT](https://jwt.io/)
- [Cracking JWT](https://www.sjoerdlangkemper.nl/2016/09/28/attacking-jwt-authentication/)
