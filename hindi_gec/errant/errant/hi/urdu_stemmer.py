import re

class UrduStemmer:
    def __init__(self):
        self.urduPrefixes = ['بے', 'بد', 'لا', 'ے', 'نا', 'با', 'کم', 'ان', 'اہل', 'کم']
        self.urduSuffixes = ['دار', 'وں', 'یاں', 'یں', 'ات', 'گوار', 'ور', 'پسند']
        self.allUrduAffixes = {}

    def remove_space(self, string):
        return string.replace(" ", "")

    def load_urdu_affixes(self, file_path):
        urduFile = open(file_path, "r", encoding="utf-8")
        for urduWord in urduFile:
            x = urduWord.strip().split('\t\t')
            self.allUrduAffixes[x[0]] = x[1]

    def stem(self, urduWord):
        prefixFound = False

        for prefix in self.urduPrefixes:
            checkPrefix = re.search(rf'\A{prefix}', urduWord)
            if checkPrefix:
                predictedStem = urduWord[checkPrefix.span(0)[1]:]
                prefixFound = True
                #realStem = self.remove_space(self.allUrduAffixes.get(urduWord, ""))
                predictedStem = self.remove_space(predictedStem)
                return predictedStem

        if not prefixFound:
            for suffix in self.urduSuffixes:
                checkSuffix = re.search(rf"{suffix}\Z", urduWord)
                if checkSuffix:
                    predictedStem = urduWord[:checkSuffix.span(0)[0]]
                    #realStem = self.remove_space(self.allUrduAffixes.get(urduWord, ""))
                    predictedStem = self.remove_space(predictedStem)
                    return predictedStem

        return urduWord
