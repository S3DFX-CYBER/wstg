# REST सुरक्षा परीक्षण गाइड (REST Testing Guide – सरल हिंदी)

## परिचय

Web Services का उपयोग अलग-अलग applications के बीच डेटा भेजने और लेने के लिए किया जाता है।  
इनका उपयोग मशीन-से-मशीन (machine-to-machine) communication के लिए होता है।

REST (Representational State Transfer) एक सरल और हल्का तरीका है Web Services बनाने का।  
यह सामान्य HTTP requests का उपयोग करता है, इसलिए इसे समझना और उपयोग करना आसान होता है।

REST APIs का उपयोग:
- Web applications
- Mobile apps
- Desktop apps
- Backend services

---

## REST API कैसे काम करती है?

REST APIs HTTP methods का उपयोग करती हैं:

- **GET** – डेटा प्राप्त करने के लिए  
- **POST** – नया डेटा बनाने के लिए  
- **PUT / PATCH** – डेटा अपडेट करने के लिए  
- **DELETE** – डेटा हटाने के लिए  

डेटा आमतौर पर इन formats में होता है:
- JSON (सबसे सामान्य)
- XML

Parameters इन जगहों पर हो सकते हैं:
- URL में
- Request headers में
- Request body में

Authentication आमतौर पर:
- API Token
- JWT
- Bearer Token

---

## REST APIs की सुरक्षा परीक्षण क्यों मुश्किल है?

REST APIs का security testing चुनौतीपूर्ण हो सकता है क्योंकि:

- सभी endpoints दिखाई नहीं देते
- कुछ APIs केवल client-side code से call होती हैं
- Mobile या desktop apps का code inspect करना कठिन होता है
- Parameters standard format में नहीं होते
- JSON में बहुत सारे fields हो सकते हैं
- Custom authentication tools को सही तरह काम करने से रोक सकती है

---

## REST API Pentesting कैसे करें?

### 1. Documentation खोजें

अगर उपलब्ध हो तो:

- API documentation
- Developer guide
- Source code या configuration files

इससे API structure और attack surface समझने में मदद मिलती है।

---

### 2. Proxy का उपयोग करें

OWASP ZAP या Burp Suite जैसे tools का उपयोग करें:

- सभी requests capture करें
- Headers, body और parameters देखें
- केवल URL पर निर्भर न रहें

---

### 3. Attack Surface पहचानें

Captured requests को analyze करें:

- असामान्य headers खोजें
- URL में बार-बार बदलने वाले हिस्से देखें

उदाहरण:https://example.com/api/user/123

यहाँ `123` एक parameter हो सकता है।

ध्यान दें:

- JSON या XML data
- Extension के बिना URLs
- Variable URL segments

---

### 4. Parameters की जांच करें

Test करें:

- गलत values भेजें
- खाली values भेजें
- unexpected data types भेजें

Response देखें:

- **404 Error** → Path गलत है  
- **Application error** → Parameter validation हो रहा है  

---

### 5. Fuzzing की तैयारी

Fuzzing करते समय:

- Valid और invalid values पहचानें
- Edge cases test करें:
  - Negative numbers
  - बहुत बड़े values
  - Empty strings
  - Special characters

अगर JSON है, तो हर field को test करें।

---

### 6. Authentication को संभालें

Testing करते समय:

- Valid token उपयोग करें
- Session expire होने पर नया token लें
- Authentication flow को बनाए रखें

---

## Testing के दौरान क्या देखें?

- Input validation की कमी
- Authorization issues (IDOR)
- Rate limiting की कमी
- Sensitive data exposure
- Error messages में internal information
- SSRF या injection की संभावना

---

## उपयोगी Tools

- OWASP ZAP  
- Burp Suite  
- Postman  
- Curl  

---

## अतिरिक्त संसाधन

REST Security Cheat Sheet:  
https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html

REST Security पर वीडियो:  
https://www.youtube.com/watch?v=pWq4qGLAZHI

---

## नोट

यह गाइड शुरुआती और मध्यम स्तर के learners के लिए बनाई गई है ताकि वे REST APIs की सुरक्षा को समझ सकें और basic testing शुरू कर सकें।