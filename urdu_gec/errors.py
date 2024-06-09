common_words_dict = {
    ' کے ': ' کا ',
    ' کا ': ' کے ',
    ' میں ': ' مے ',
    ' مے ': ' میں ',
    ' کی ': ' کا ',
    ' سے ': ' سی ',
    ' اس ': ' وہ ',
    ' اور ': ' و ',
    ' نے ': ' نا ',
    ' کر ': ' کو ',
    ' کو ': ' کی ',
    ' وہ ': ' و ',
    ' تو ': ' جو ',
    ' کہ ': ' کے ',
    ' ایک ': ' یک ',
     ' یک ' : ' ایک ',
    ' بھی ': ' تھی ',
    ' پر ': ' مر ',
    ' یہ ': ' وہ ',
    ' نہیں ': ' نہ ',
    ' ان ': ' کن ',
    ' ہی ': ' ہا ',
    ' تھا ': ' تھی ',
    ' تھی ': ' تھا ',
    ' بہت ': ' بھت ',
    ' تھا ': ' تھی ',
    ' تھی ': ' تھا ',
    ' ہو ': ' جو ',
    ' ہے ': 'ھو ' ,
    ' اپنے ': ' اپنا ',
    ' اپنا ': ' اپنے ',
    ' اسے ': ' اس نے ',
    ' کیا ': ' کی ',
    ' بات ': ' باتو '
}


word_error = {
    ' کا ': ' کی ',  # Incorrect use of gender (مذکر vs. مونث)
    ' کی ': ' کا ',  # Incorrect use of gender (مذکر vs. مونث)
    ' گزرے ': ' گزری ',  # Incorrect verb agreement in past tense
    ' گزری ': ' گزرے ',  # Incorrect verb agreement in past tense
    ' کیا ': ' کرا ',  # Incorrect verb choice
    ' تھا ': ' تھی ',  # Incorrect use of gender (مذکر vs. مونث)
    ' تھی ': ' تھا ',  # Incorrect use of gender (مذکر vs. مونث)
    ' ؟ ': ' ',  # Incorrect use of question mark
    ' دیا ': ' دی ',  # Incorrect use of gender (مذکر vs. مونث)
    ' دی ': ' دیا ',  # Incorrect use of gender (مذکر vs. مونث)
    ' اسے ': ' اس نے ',  # Incorrect use of pronoun
    ' مجھے ': ' میں نے ',  # Incorrect use of pronoun
    ' ہیں ': ' ہے ',  # Incorrect use of gender (مذکر vs. مونث)
    ' ہے ': ' ہیں ',  # Incorrect use of gender (مذکر vs. مونث)
    ' ملی ': ' ملا ',  # Incorrect use of gender (مذکر vs. مونث)
    ' ملا ': ' ملی ',  # Incorrect use of gender (مذکر vs. مونث)
    ' خریدا ': ' خریدی ',  # Incorrect use of gender (مذکر vs. مونث)
    ' خریدی ': ' خریدا ',  # Incorrect use of gender (مذکر vs. مونث)
    ' پڑتی ': ' پڑتا ',  # Incorrect use of gender (مذکر vs. مونث)
    ' پڑتا ': ' پڑتی ',  # Incorrect use of gender (مذکر vs. مونث)
    ' پرھتا ': ' پڑھتے ',  # Incorrect verb agreement in present tense
    ' پڑھتی ': ' پڑھتا ',  # Incorrect verb agreement in present tense
    ' اونچی ': ' اونچا ',  # Incorrect use of gender (مذکر vs. مونث)
    ' اونچا ': ' اونچی ',  # Incorrect use of gender (مذکر vs. مونث)
    ' ہوتی ': ' ہوتا ',  # Incorrect use of gender (مذکر vs. مونث)
    ' ہوتا ': ' ہوتی ',  # Incorrect use of gender (مذکر vs. مونث)
    ' بھاگی ': ' بھاگا ',  # Incorrect use of gender (مذکر vs. مونث)
    ' بھاگا ': ' بھاگی ',  # Incorrect use of gender (مذکر vs. مونث)
    ' دیں ': ' دے ',  # Incorrect verb agreement in present tense
    ' دے ': ' دیں ',  # Incorrect verb agreement in present tense
    ' لگا ': ' لگی ',
    ' لگی ': ' لگا ',
    ' کرتا ': ' کرتی ',
    ' کرتی ': ' کرتا ',
    ' کھاتا ': ' کھاتی ',
    ' کھاتی ': ' کھاتا ',
    ' ہوئے ': ' ہوئیں ',
    ' ہوئیں ': ' ہوئے ',
    ' گئی ': ' گیا ',
    ' گیا ': ' گئی ',
    ' آئی ': ' آیا ',
    ' آیا ': ' آئی ',
    ' آتا ': ' آتی ',
    ' آتی ': ' آتا ',
    ' کھیلتا ': ' کھیلتی ',
    ' کھیلتی ': ' کھیلتا ',
    ' کہتا ': ' کہتی ',
    ' کہتی ': ' کہتا ',
    ' پکڑتا ': ' پکڑتی ',
    ' پکڑتی ': ' پکڑتا ',
    ' پڑھتا ہے ': ' پڑھتی ہے ',
    ' پڑھتی ہے ': ' پڑھتا ہے ',
    ' پھولتا ': ' پھولتی ',
    ' پھولتی ': ' پھولتا ',
    ' رہتا ': ' رہتی ',
    ' رہتی ': ' رہتا ',
    ' بولتا ': ' بولتی ',
    ' بولتی ': ' بولتا ',
    ' لڑکیاں ': ' لڑکے ',  # Incorrect plural form
    ' لڑکے ': ' لڑکیاں ',  # Incorrect plural form
    ' کتابیں ': ' کتاب ',  # Incorrect plural form
    ' کتاب ': ' کتابیں ',  # Incorrect plural form
    ' پھولوں ': ' پھول ',  # Incorrect plural form
    ' پھول ': ' پھولوں ',  # Incorrect plural form
    ' مکھیوں ': ' مکھی ',  # Incorrect plural form
    ' مکھی ': ' مکھیوں ',
    ' سڑکیں ': ' سڑک ',  # Incorrect plural form
    ' سڑک ': ' سڑکیں ',  # Incorrect plural form
    ' بچیاں ': ' بچے ',  # Incorrect plural form
    ' بچے ': ' بچیاں ',  # Incorrect plural form
    ' کرسیاں ': ' کرسی ',  # Incorrect plural form
    ' کرسی ': ' کرسیاں ',  # Incorrect plural form
    ' ماشینیں ': ' ماشین ',  # Incorrect plural form
    ' ماشین ': ' ماشینیں ',  # Incorrect plural form
    ' باغات ': ' باغ ',  # Incorrect plural form
    ' باغ ': ' باغات ',  # Incorrect plural form
    ' دوستوں ': ' دوست ',  # Incorrect plural form
    ' دوست ': ' دوستوں ',  # Incorrect plural form
    ' آسمانیں ': ' آسمان ',  # Incorrect plural form
    ' آسمان ': ' آسمانیں ',  # Incorrect plural form
    ' راستے ': ' راستا ',  # Incorrect plural form
    ' راستا ': ' راستے ',  # Incorrect plural form
    ' رہی ': ' رہا ',
    ' رہا ': ' رہی ',
    ' کرے ': ' کریں ',
    ' کریں ': ' کرے ',
    ' میرا ':' میری ',
    ' میری ':' میرا ',
    ' میرے ':' میرا ',
    ' اسکا ':' اسکی ',
    ' اسکی ':' اسکا ',
    ' اسکے ':' اسکا ',
    ' ہمارا ':' ہمارے ',
    ' ہمارے ':' ہمارا ',
    ' ہماری ':' ہمارا ',
    ' تمہارا ':' تمہاری ',
    ' تمہاری ':' تمہارا ',
    ' تمہارے ':' تمہارا ',
    ' انکا ':' انکی ',
    ' انکی ':' انکا ',
    ' انکے ':' انکا ',
}
