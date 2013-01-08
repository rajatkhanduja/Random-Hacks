#!/usr/bin/python
# Author : Rajat Khanduja
# This program requires spam and ham stored in files named "spam" and "ham"
# respectively, in the current folder.

# Call to program
# python spamClassifier <spamPrior> <testFile>

#    Copyright (C) 2013 Rajat Khanduja
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.



import sys

def createDictionay(fileName):
  f = open (fileName)
  all_words = map(lambda l: l.split(" "), f.readlines())
  knownWords = dict()
  for line in all_words:
    for word in line:
      word = word.lower()
      if word in knownWords:
        knownWords[word] += 1
      else:
        knownWords[word] = 1
  return knownWords

class NaiveBayesModel:
  def __init__ (self, p, pFeature1, pFeature2, pFeature):
    self.p = p
    self.pFeature1 = pFeature1
    self.pFeature2 = pFeature2
    self.pFeature  = pFeature

  def classify (self, inputFeatures):
    prob1 = self.p
    prob2 = 1 - self.p

    for feature in inputFeatures:
      if feature in self.pFeature:
        prob1 *= (self.pFeature1[feature] / self.pFeature[feature])
        prob2 *= (self.pFeature2[feature] / self.pFeature[feature])

    if prob1 > prob2:
      return True
    else:
      return False


def laplacianSmoothenedProbability (wordCount):
  totalCount = 0
  totalWords = 0
  for word in wordCount:
    wordCount[word] += 1
    totalCount += wordCount[word]
  
  probabilities = dict()
  for word in wordCount:
    probabilities[word] = wordCount[word] * 1.0 / totalCount
  
  return probabilities
  

def main(args):
  priorSpam = float(args[1])
  
  spamWords = createDictionay ("spam")
#  print "Created Spam dictionary"
  hamWords  = createDictionay ("ham")
#  print "Created Ham Dictionary"
  words     = dict()

  for word in hamWords:
    if word not in spamWords:
      spamWords[word] = 0
    words[word] = hamWords[word]
  
  for word in spamWords:
    if word not in hamWords:
      hamWords[word] = 0

    if word in words:
      words[word] += spamWords[word]
    else:
      words[word]  = spamWords[word]
  
#  print "Merged"

  spamWordsProb = laplacianSmoothenedProbability (spamWords)
  hamWordsProb  = laplacianSmoothenedProbability (hamWords)
  wordsProb     = laplacianSmoothenedProbability (words)

#  print "Created Probabilities"

  nb = NaiveBayesModel (priorSpam, spamWordsProb, hamWordsProb, wordsProb)

  testFile = open (args[2])
  lines = testFile.readlines()
  for line in lines:
    words = line.split()
    if nb.classify(words):
#      print "spam"
    else:
#      print "ham"
    


if __name__ == "__main__":
  main (sys.argv)
