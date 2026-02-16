# स्टाइल गाइड

Web Security Testing Guide (WSTG) एक प्रसिद्ध दस्तावेज है जिस पर दुनिया भर के सुरक्षा पेशेवरों और संगठनों का भरोसा है। ये दिशानिर्देश यह सुनिश्चित करने में मदद करते हैं कि यह अपने कई योगदानकर्ताओं और सुरक्षा समुदाय को अच्छी तरह से प्रतिबिंबित करे।

WSTG की गुणवत्ता बनाए रखने के लिए, कृपया इन सामान्य नियमों का पालन करें।

1. तथ्यात्मक, विशिष्ट रहें और सुनिश्चित करें कि paragraphs अपने heading पर केंद्रित हों।
2. सुनिश्चित करें कि जानकारी विश्वसनीय और अद्यतित है। जहां उचित हो links और citations प्रदान करें।
3. सामग्री को दोहराने से बचें। मौजूदा सामग्री का संदर्भ देने के लिए, इसे inline link करें।

## पाठक के लिए लिखें

WSTG के पाठक कई अलग-अलग देशों से आते हैं और उनके पास तकनीकी विशेषज्ञता के अलग-अलग स्तर होते हैं। बुनियादी तकनीकी पृष्ठभूमि वाले अंतर्राष्ट्रीय दर्शकों के लिए लिखें। ऐसे शब्दों का उपयोग करें जो गैर-देशी अंग्रेजी बोलने वाले द्वारा समझे जाने की संभावना हो। छोटे वाक्यों का उपयोग करें जो समझने में आसान हों।

वेब टूल [Hemingway](https://hemingwayapp.com/) आपको स्पष्टता के साथ लिखने में मदद कर सकता है।

## फॉर्मेटिंग

हमें सामग्री की समीक्षा और प्रकाशित करने में मदद के लिए और पाठकों को जानकारी समझने में मदद के लिए consistent formatting का उपयोग करें। सभी सामग्री को [Markdown syntax](https://guides.github.com/features/mastering-markdown/#examples) का उपयोग करके लिखें।

कृपया formatting के लिए इन अतिरिक्त दिशानिर्देशों का पालन करें।

### Article Template

हम विषयों को पूर्ण और समझने में आसान बनाने में मदद के लिए एक article template का उपयोग करते हैं। कृपया नई सामग्री को structure करने के लिए [template materials](template) का उपयोग करें।

### Project Folder Structure

Articles और images जोड़ते समय, कृपया articles को उपयुक्त sub-section directory में रखें। Images को article directory के भीतर `images/` folder में रखें। यहाँ project structure का एक उदाहरण है:

```sh
document/
 ├───0_Foreword/
 │   └───0_Foreword.md
 ├───1_Frontispiece/
 │   ├───images/
 │   │   └───example.jpg
 │   └───1_Frontispiece.md
 ├───2_Introduction/
 │   ├───images/
 │   │   └───example.jpg
 │   └───2_Introduction.md
 ├───3_The_OWASP_Testing_Framework/
 │   ├───images/
 │   │   └───example.jpg
 │   └───3_The_OWASP_Testing_Framework.md
 ├───4_Web_Application_Security_Testing/
 │   ├───4.1_Introduction_and_Objectives/
 │   │   └───4.1_Testing_Introduction_and_Objectives.md
 │   ├───4.2_Information_Gathering/
 │   │   ├───images/
 │   │   │   └───example.jpg
 │   │   ├───4.2_Testing_Information_Gathering.md
 │   │   └───4.2.1_Conduct_Search_Engine_Discovery.md

```

### Code Syntax Highlighting

Snippets के लिए syntax highlighting के साथ code fences का उपयोग करें। उदाहरण के लिए:

```md
    ```javascript
    if (isAwesome){
        return true
    }
    ```
```

### Caption Images

Title case का उपयोग करके images और figures को caption करें। Section और sub-section numbers का उपयोग करें, इसके बाद document में figure की position। Format `Figure <section>.<sub-section>-<position>: Caption Title` का उपयोग करें।

उदाहरण के लिए, section 4.8, sub-section 19 में दिखाई गई पहली image को इस प्रकार caption करें:

```md
![SSTI XVWA Example](images/SSTI_XVWA.jpeg)\
*Figure 4.7.19-1: SSTI XVWA Example*
```

### Inline Links

Links को inline जोड़ें। उन्हें describe करने के लिए वाक्य में शब्दों का उपयोग करें, या उनके specific title को शामिल करें। उदाहरण के लिए:

```md
This project provides a [style guide](style_guide.md). Some style choices are taken from the [Chicago Manual of Style](https://www.chicagomanualofstyle.org/).
```

### Inline References

जिन resources के लिए link उपलब्ध नहीं है, जैसे कि whitepaper या book, हम किसी भी academic-styled citation के बजाय conversational in-line reference पसंद करते हैं। Resource के title के साथ-साथ इसके author को अपने text में शामिल करें। उदाहरण के लिए:

> तीन संभावित cases हैं: केवल whale मौजूद है, केवल petunias मौजूद हैं, या whale और petunias दोनों एक साथ मौजूद हैं। इन possibilities का संदर्भ *The Hitchhiker's Guide to the Galaxy* नामक पुस्तकों की एक श्रृंखला में दिया गया है, जो Douglas Adams द्वारा लिखी गई है।

इस format का फायदा यह है कि यह article के flow को जारी रखता है और पाठकों को paragraph से paragraph तक jump करने, asterisk खोजने, या reference list खोजने के लिए किसी अन्य location पर जाने के लिए आमंत्रित नहीं करता है। यह पढ़ने और maintain करने में भी आसान है क्योंकि यह केवल एक ही स्थान पर दिखाई देता है।

### Bold, Italic, और Underline

Emphasis के लिए bold, italic, या underlined text का उपयोग न करें।

आप किसी शब्द का refer करते समय उसे italicize कर सकते हैं, हालांकि technical writing में इसकी आवश्यकता दुर्लभ है। उदाहरण के लिए, section [Use Correct Words](#use-correct-words) देखें। Asterisks का उपयोग करें: `*italic*`।

## भाषा और व्याकरण

WSTG को consistent और पढ़ने में सुखद बनाने के लिए, कृपया अपनी spelling की जांच करें (हम American English का उपयोग करते हैं) और उचित grammar का उपयोग करें।

नीचे दिए गए sections में follow करने के लिए specific style choices का वर्णन है।

### Title Case

Headings के लिए title case का उपयोग करें, [Chicago Manual of Style](https://www.chicagomanualofstyle.org/book/ed17/frontmatter/toc.html) का पालन करते हुए। Website [Capitalize My Title](https://capitalizemytitle.com/#Chicago) पर "Chicago" tab मदद कर सकता है।

### Active Voice

Passive voice का उपयोग करने से बचें। उदाहरण के लिए:

> खराब: "Vulnerabilities are found by running tests."  
> अच्छा: "Run tests to find vulnerabilities."  

### Second Person

First या third person में न लिखें, जैसे *I* या *he* का उपयोग करके। Technical instruction देते समय, reader को second person में address करें। [Zero या implied subject](https://en.wikipedia.org/wiki/Subject_(grammar)#Forms_of_the_subject) का उपयोग करें, या यदि आवश्यक हो, तो *you* का उपयोग करें।

> खराब: "He/she/an IT monkey would run this code to test..."  
> बेहतर: "By running this code, you can test..."  
> सर्वश्रेष्ठ: "Run this code to test..."

### Numbering Conventions

Zero से ten तक के numbers के लिए, शब्द लिखें। Ten से अधिक numbers के लिए, integers का उपयोग करें। उदाहरण के लिए:

> One broken automated test finds 42 errors if you run it ten times.

Simple fractions को शब्दों में describe करें। उदाहरण के लिए:

> Half of all software developers like petunias, and a third of them like whales.

Monetary value के approximate magnitude का वर्णन करते समय, पूरा शब्द लिखें और abbreviate न करें। उदाहरण के लिए:

> खराब: "Security testing saves companies $18M in beer every year."  
> अच्छा: "Security testing saves companies eighteen million dollars in beer every year."

Specific monetary value के लिए, currency symbols और integers का उपयोग करें। उदाहरण के लिए:

> A beer costs $6.75 today, and $8.25 tomorrow.

### Abbreviations

Abbreviations को पहली बार अपने document में प्रकट होने पर explain करें। Abbreviated form को indicate करने के लिए उपयुक्त शब्दों को capitalize करें। उदाहरण के लिए:

> This project contains the source code for the Web Security Testing Guide (WSTG). The WSTG is a nice and accurate book.

### Lists और Punctuation

जब order महत्वहीन हो तो bulleted lists का उपयोग करें। Sequential steps के लिए numbered lists का उपयोग करें। प्रत्येक line के लिए, पहले शब्द को capitalize करें। यदि line एक sentence है या sentence को complete करती है, तो period के साथ समाप्त करें। उदाहरण के लिए:

> Testing this scenario will:
>
> - Make the application safer.
> - Improve overall security posture.
> - Keep customers happy.
>
> To test this scenario:
>
> 1. Copy the code.
> 2. Open a terminal.
> 3. Run the code as root.
>
> Here are some foods to snack on while testing.
>
> - Apples
> - Beef jerky
> - Chocolate

एक sentence में lists के लिए, serial या [Oxford commas](https://www.grammarly.com/blog/what-is-the-oxford-comma-and-why-do-people-care-so-much-about-it/) का उपयोग करें। उदाहरण के लिए:

> Test the application using automated tests, static code review, and penetration tests.

### सही शब्दों का उपयोग करें

निम्नलिखित section में कुछ अक्सर गलत उपयोग किए जाने वाले शब्द और उन्हें सही तरीके से उपयोग करने के निर्देश शामिल हैं।

#### *and/or*

जबकि कभी-कभी legal documents में उपयोग किया जाता है, *and/or* technical writing में अस्पष्टता और भ्रम की ओर ले जाता है। इसके बजाय, *or* का उपयोग करें, जो English भाषा में *and* को शामिल करता है। उदाहरण के लिए:

> खराब: "The code will output an error number and/or description."  
> अच्छा: "The code will output an error number or description."

बाद वाला sentence error number और description दोनों होने की possibility को exclude नहीं करता है।

यदि आपको सभी संभावित outcomes को specify करने की आवश्यकता है, तो list का उपयोग करें:

> "The code will output an error number, or a description, or both."

#### *frontend, backend*

जबकि यह सच है कि English भाषा समय के साथ विकसित होती है, ये अभी तक शब्द नहीं हैं।

Nouns का refer करते समय, *front end* और *back end* का उपयोग करें। उदाहरण के लिए:

> Security is equally important on the front end as it is on the back end.

Descriptive adverb के रूप में, hyphenated *front-end* और *back-end* का उपयोग करें।

> Both front-end developers and back-end developers are responsible for application security.

#### *whitebox*, *blackbox*, *greybox*

ये शब्द नहीं हैं।

Nouns के रूप में, *white box*, *black box*, और *grey box* का उपयोग करें। ये nouns cybersecurity के संबंध में शायद ही कभी दिखाई देते हैं।

> My cat enjoys jumping into that grey box.

Adverbs के रूप में, hyphenated *white-box*, *black-box*, और *grey-box* का उपयोग करें। Capitalization का उपयोग न करें जब तक कि शब्द title में न हों।

> While white-box testing involves knowledge of source code, black-box testing does not. A grey-box test is somewhere in-between.

#### *ie*, *eg*

ये letters हैं।

Abbreviation *ie* Latin `id est` को refer करता है, जिसका अर्थ है "in other words"। Abbreviation *eg* `exempli gratia` के लिए है, जिसका अनुवाद "for example" है। इन्हें एक sentence में उपयोग करने के लिए:

> Write using proper English, i.e. correct spelling and grammar. Use common words over uncommon ones, e.g. "learn" instead of "glean."

#### *etc*

ये भी letters हैं।

Latin phrase *et cetera* का अनुवाद "and the rest" है। इसे abbreviated किया जाता है और typically एक list के अंत में रखा जाता है जिसे complete करना redundant लगता है:

> WSTG authors like rainbow colors, such as red, yellow, green, etc.

Technical writing में, *etc* का उपयोग problematic है। यह मान लेता है कि reader जानता है कि आप किस बारे में बात कर रहे हैं, और वे नहीं जान सकते हैं। Violet rainbow के colors में से एक है, लेकिन ऊपर दिया गया example आपको स्पष्ट रूप से नहीं बताता है कि violet एक ऐसा color है जो WSTG authors को पसंद है।

Explicit और thorough होना reader के बारे में assumptions बनाने से बेहतर है। *etc* का उपयोग केवल एक list को complete करने से बचने के लिए करें जो document में पहले पूर्ण रूप से दी गई थी।

#### *...* (ellipsis)

Ellipsis punctuation mark indicate कर सकता है कि quote से शब्द छोड़ दिए गए हैं:

> Linus Torvalds once said, "Once you realize that documentation should be laughed at... THEN, and only then, have you reached the level where you can safely read it and try to use it to actually implement a driver."

जब तक omission quote के meaning को नहीं बदलता है, यह WSTG में ellipsis का acceptable usage है।

Ellipsis के अन्य सभी uses, जैसे कि एक unfinished thought को indicate करना, नहीं हैं।

#### *ex*

जबकि यह एक शब्द है, यह संभवतः वह शब्द नहीं है जिसे आप खोज रहे हैं। शब्द *ex* का finance और commerce के क्षेत्रों में particular meaning है, और यदि आप अपने past relationships पर चर्चा कर रहे हैं तो यह एक person को refer कर सकता है। इनमें से कोई भी topic WSTG में दिखाई नहीं देना चाहिए।

Abbreviation को lazy writers द्वारा "example" के लिए mean करने के लिए उपयोग किया जा सकता है। कृपया lazy न बनें, और इसके बजाय *example* लिखें।
