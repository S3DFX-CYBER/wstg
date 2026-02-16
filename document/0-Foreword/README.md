# प्रस्तावना

असुरक्षित software की समस्या शायद हमारे समय की सबसे महत्वपूर्ण तकनीकी चुनौती है। Business, social networking आदि को सक्षम करने वाले web applications की नाटकीय वृद्धि ने हमारे internet, web applications और data को लिखने और सुरक्षित करने के लिए एक मजबूत दृष्टिकोण स्थापित करने की आवश्यकताओं को और बढ़ा दिया है।

Open Worldwide Application Security Project® (OWASP®) में, हम दुनिया को एक ऐसी जगह बनाने की कोशिश कर रहे हैं जहाँ असुरक्षित software एक anomaly (अपवाद) हो, सामान्य नहीं। इस गंभीर मुद्दे को हल करने में OWASP Testing Guide की एक महत्वपूर्ण भूमिका है। यह बेहद महत्वपूर्ण है कि सुरक्षा मुद्दों के लिए software का परीक्षण करने का हमारा दृष्टिकोण engineering और science के सिद्धांतों पर आधारित हो। हमें web applications का परीक्षण करने के लिए एक consistent, दोहराने योग्य और परिभाषित दृष्टिकोण की आवश्यकता है। Engineering और technology के मामले में कुछ न्यूनतम मानकों के बिना एक दुनिया अराजकता की दुनिया है।

यह कहने की आवश्यकता नहीं है कि आप इस पर सुरक्षा परीक्षण किए बिना एक सुरक्षित application नहीं बना सकते हैं। Testing एक सुरक्षित system बनाने के व्यापक दृष्टिकोण का हिस्सा है। कई software development organizations अपनी मानक software development process के हिस्से के रूप में सुरक्षा परीक्षण को शामिल नहीं करते हैं। इससे भी बदतर यह है कि कई सुरक्षा vendors गुणवत्ता और rigor की अलग-अलग degrees के साथ परीक्षण प्रदान करते हैं।

सुरक्षा परीक्षण, अपने आप में, एक application कितना सुरक्षित है इसका विशेष रूप से अच्छा stand alone measure नहीं है, क्योंकि एक attacker के पास application को तोड़ने के अनगिनत तरीके हो सकते हैं, और उन सभी का परीक्षण करना संभव नहीं है। हम खुद को सुरक्षित नहीं hack कर सकते क्योंकि हमारे पास परीक्षण और रक्षा करने के लिए सीमित समय होता है जबकि एक attacker के पास ऐसी बाधाएं नहीं होती हैं।

अन्य OWASP projects जैसे Code Review Guide, Development Guide और [ZAP](https://www.zaproxy.org/) जैसे tools के साथ, यह सुरक्षित applications बनाने और maintain करने की दिशा में एक शानदार शुरुआत है। यह Testing Guide आपको दिखाएगा कि अपने running application की सुरक्षा को कैसे verify करें। मैं अत्यधिक सिफारिश करता हूं कि इन guides का उपयोग अपनी application security initiatives के हिस्से के रूप में करें।

## OWASP क्यों?

इस तरह की guide बनाना एक विशाल undertaking है, जिसके लिए दुनिया भर के सैकड़ों लोगों की expertise की आवश्यकता होती है। सुरक्षा खामियों के परीक्षण के कई अलग-अलग तरीके हैं और यह guide इस बात की consensus को capture करता है कि इस परीक्षण को जल्दी, सटीक और कुशलता से कैसे किया जाए। OWASP समान विचारधारा वाले सुरक्षा लोगों को एक साथ काम करने और एक सुरक्षा समस्या के लिए एक leading practice दृष्टिकोण बनाने की क्षमता देता है।

इस guide को पूरी तरह से free और open तरीके से उपलब्ध कराना foundation के mission के लिए महत्वपूर्ण है। यह किसी को भी सामान्य सुरक्षा मुद्दों के परीक्षण के लिए उपयोग की जाने वाली techniques को समझने की क्षमता देता है। Security एक black art या बंद रहस्य नहीं होना चाहिए जिसे केवल कुछ लोग ही practice कर सकें। यह सभी के लिए open होना चाहिए और न केवल security practitioners के लिए exclusive होना चाहिए बल्कि QA, Developers और Technical Managers के लिए भी। इस guide को बनाने की project इस expertise को उन लोगों के हाथों में रखती है जिन्हें इसकी आवश्यकता है - आप, मैं और कोई भी जो software बनाने में शामिल है।

यह guide developers और software testers के हाथों में पहुंचनी चाहिए। समग्र समस्या में कोई महत्वपूर्ण प्रभाव डालने के लिए दुनिया में पर्याप्त application security experts नहीं हैं। Application security की प्रारंभिक जिम्मेदारी developers के कंधों पर आनी चाहिए क्योंकि वे code लिखते हैं। यह आश्चर्यजनक नहीं होना चाहिए कि developers सुरक्षित code नहीं बना रहे हैं यदि वे इसके लिए परीक्षण नहीं कर रहे हैं या उन प्रकार के bugs पर विचार नहीं कर रहे हैं जो vulnerability को introduce करते हैं।

इस जानकारी को up to date रखना इस guide project का एक critical पहलू है। Wiki approach को अपनाकर, OWASP community इस guide में जानकारी को evolve और expand कर सकती है ताकि तेजी से बदलते application security threat landscape के साथ तालमेल बनाए रख सके।

यह Guide हमारे members और project volunteers की इस विषय के लिए passion और energy का एक महान प्रमाण है। यह निश्चित रूप से एक समय में code की एक line से दुनिया को बदलने में मदद करेगा।

## अनुकूलन और प्राथमिकता

आपको अपने organization में इस guide को adopt करना चाहिए। आपको अपने organization की technologies, processes और organizational structure से मेल खाने के लिए जानकारी को tailor करने की आवश्यकता हो सकती है।

सामान्य तौर पर organizations के भीतर कई अलग-अलग roles होते हैं जो इस guide का उपयोग कर सकते हैं:

- Developers को यह सुनिश्चित करने के लिए इस guide का उपयोग करना चाहिए कि वे सुरक्षित code बना रहे हैं। ये tests सामान्य code और unit testing procedures का हिस्सा होना चाहिए।
- Software testers और QA को applications पर लागू किए जाने वाले test cases के set को expand करने के लिए इस guide का उपयोग करना चाहिए। इन vulnerabilities को जल्दी पकड़ने से बाद में काफी समय और प्रयास की बचत होती है।
- Security specialists को अन्य techniques के साथ इस guide का उपयोग यह verify करने के एक तरीके के रूप में करना चाहिए कि एक application में कोई सुरक्षा छेद नहीं छूटा है।
- Project Managers को इस बात पर विचार करना चाहिए कि यह guide क्यों मौजूद है और यह कि सुरक्षा मुद्दे code और design में bugs के माध्यम से प्रकट होते हैं।

सुरक्षा परीक्षण करते समय याद रखने वाली सबसे महत्वपूर्ण बात लगातार re-prioritize करना है। एक application के fail होने के अनंत तरीके हो सकते हैं, और organizations के पास हमेशा सीमित परीक्षण समय और resources होते हैं। सुनिश्चित करें कि समय और resources का बुद्धिमानी से खर्च किया जाए। उन सुरक्षा छेदों पर focus करने का प्रयास करें जो आपके business के लिए एक वास्तविक जोखिम हैं। Application और इसके use cases के संदर्भ में risk को contextualize करने का प्रयास करें।

इस guide को techniques के एक set के रूप में देखा जाना सबसे अच्छा है जिसका उपयोग आप विभिन्न प्रकार के सुरक्षा छेदों को खोजने के लिए कर सकते हैं। लेकिन सभी techniques समान रूप से महत्वपूर्ण नहीं हैं। Guide को एक checklist के रूप में उपयोग करने से बचने का प्रयास करें, नई vulnerabilities हमेशा प्रकट होती रहती हैं और कोई भी guide "परीक्षण के लिए चीजों" की exhaustive list नहीं हो सकती है, बल्कि शुरू करने के लिए एक शानदार जगह है।

## Automated Tools की भूमिका

कई companies automated security analysis और testing tools बेच रही हैं। इन tools की सीमाओं को याद रखें ताकि आप उन्हें उसके लिए उपयोग कर सकें जिसमें वे अच्छे हैं। जैसा कि Michael Howard ने Seattle में 2006 OWASP AppSec Conference में कहा था, "Tools software को सुरक्षित नहीं बनाते हैं! वे process को scale करने में मदद करते हैं और policy को enforce करने में मदद करते हैं।"

सबसे महत्वपूर्ण बात यह है कि ये tools generic हैं - मतलब कि वे आपके custom code के लिए नहीं बल्कि सामान्य रूप से applications के लिए designed हैं। इसका मतलब है कि जबकि वे कुछ generic problems खोज सकते हैं, उनके पास आपके application के बारे में पर्याप्त knowledge नहीं है जो उन्हें अधिकांश flaws का पता लगाने की अनुमति दे। मेरे अनुभव में, सबसे गंभीर सुरक्षा मुद्दे वे हैं जो generic नहीं हैं, बल्कि आपके business logic और custom application design में गहराई से जुड़े हुए हैं।

ये tools बहुत उपयोगी भी हो सकते हैं, क्योंकि वे बहुत सारे संभावित मुद्दों को खोजते हैं। जबकि tools चलाने में ज्यादा समय नहीं लगता है, प्रत्येक संभावित समस्या की जांच और verify करने में समय लगता है। यदि लक्ष्य जल्दी से जल्दी सबसे गंभीर flaws को खोजना और समाप्त करना है, तो विचार करें कि आपका समय automated tools के साथ बेहतर खर्च किया गया है या इस guide में वर्णित techniques के साथ। फिर भी, ये tools निश्चित रूप से एक well-balanced application security program का हिस्सा हैं। बुद्धिमानी से उपयोग किए जाने पर, वे अधिक सुरक्षित code produce करने के लिए आपकी समग्र processes का समर्थन कर सकते हैं।

## कार्रवाई का आह्वान

यदि आप software बना रहे हैं, design कर रहे हैं या test कर रहे हैं, तो हम आपको दृढ़ता से प्रोत्साहित करते हैं कि इस document में सुरक्षा परीक्षण guidance से परिचित हों। यह सबसे सामान्य मुद्दों के परीक्षण के लिए एक शानदार road map है जिनका applications आज सामना कर रहे हैं, लेकिन यह exhaustive नहीं है। यदि आपको errors मिलती हैं, तो कृपया discussion page पर एक note जोड़ें या स्वयं परिवर्तन करें। आप हजारों अन्य लोगों की मदद करेंगे जो इस guide का उपयोग करते हैं।

कृपया एक individual या corporate member के रूप में [हमसे जुड़ने](https://owasp.org/membership/) पर विचार करें ताकि हम इस testing guide जैसी materials और OWASP की सभी अन्य महान projects का उत्पादन जारी रख सकें।

इस guide के सभी past और future contributors को धन्यवाद, आपका काम दुनिया भर में applications को अधिक सुरक्षित बनाने में मदद करेगा।

Open Worldwide Application Security Project और OWASP, OWASP Foundation, Inc. के registered trademarks हैं।
