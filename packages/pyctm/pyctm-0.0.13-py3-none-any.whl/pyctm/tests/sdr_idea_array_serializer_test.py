import unittest

import json
from pyctm.representation.array_dictionary import ArrayDictionary

from pyctm.representation.idea import Idea
from pyctm.representation.sdr_idea_array import SDRIdeaArray
from pyctm.representation.sdr_idea_array_deserializer import SDRIdeaArrayDeserializer
from pyctm.representation.sdr_idea_array_serializer import SDRIdeaArraySerializer
from pyctm.representation.sdr_idea_deserializer import SDRIdeaDeserializer
from pyctm.representation.sdr_idea_serializer import SDRIdeaSerializer
from pyctm.representation.dictionary import Dictionary
import numpy as np



class SDRIdeaSerializerTest(unittest.TestCase):

    def init_idea(self):

        idea = Idea(0, "Rock Music", "Hey ho let's go!", 0);
        idea.add(Idea(1, "Metallica", "Black Album", 0)).add(Idea(10, "Unforgiven", 3.14, 1)).add(Idea(3,"Enter Sadman", "Seek and destroy"))
        idea.add(Idea(4, "Foo Fighters", "The sky's the neighborhood", 0)).add(Idea(5, "Pretender", 256))
        idea.add(Idea(6, "Black Sabbath", [3.41, 2.22, 0.23], 1)).add(Idea(7, "Paranoid", [34, 18, 10]));
        idea.add(Idea(8, "Gun's in Roses", "Sweet child o' mine", 2)).add(Idea(9, "November Rain", [-18.0, 1.2, 2, 5.2, -1, 0, 1000]));
    
        return idea

    def test_sdr_serialization(self):
       
       file = open("/opt/repository/dataPlanSDR/dictionary.json")

       object=json.load(file)
       dictionary = ArrayDictionary(**object)

       sdr_idea_serializer = SDRIdeaArraySerializer(total_of_ideas=10, total_of_values=7, default_value=0, dictionary=dictionary)

       idea = self.init_idea()

       sdr_idea = sdr_idea_serializer.serialize(idea)

       print(sdr_idea)

       sdr_idea_deserializer = SDRIdeaArrayDeserializer(sdr_idea_serializer.dictionary)
       #converted_idea = sdr_idea_deserializer.deserialize(sdr_idea)

       #print(converted_idea)

       goal = np.array([ 1, 33, 33, 33,  4, 33,  4, 34, 17, 18, 33, 33, 33,  4, 33,  4, 19, 33,
         33, 33,  4, 33,  4, 35, 33, 33,  4, 33,  4, 20, 17, 21, 33, 33, 33,  4,
         33,  4, 35, 37, 33,  4, 35,  4, 33, 33, 33,  4, 33,  4, 36, 33, 33,  4,
         33,  4, 22, 17, 21, 33, 33, 33,  4, 33,  4, 37, 33, 33,  4, 33,  4, 33,
         33, 33,  4, 33,  4, 37, 33, 33,  4, 33,  4, 23, 17, 21, 33, 33, 33,  4,
         33,  4, 39, 38, 33,  4, 35,  4, 33, 33, 33,  4, 33,  4, 38, 33, 33,  4,
         33,  4, 24, 17, 21, 33, 33, 33,  4, 33,  4, 38, 33, 33,  4, 33,  4, 33,
         33, 33,  4, 33,  4, 40, 33, 33,  4, 33,  4, 25, 17, 21, 33, 33, 33,  4,
         33,  4, 38, 33, 33,  4, 33,  4, 33, 33, 33,  4, 33,  4, 39, 33, 33,  4,
         33,  4, 26, 17, 18, 33, 33, 33,  4, 33,  4, 19,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2])

       a = np.array([ 1, 45,  4, 28, 17, 21, 45,  4, 32, 17, 21, 45,  4, 32, 17, 21, 45,  4,
         32, 17, 21, 45,  4, 32, 17, 21, 45,  4, 32, 17, 21, 45,  4, 32, 17, 21,
         45,  4, 32, 17, 21, 45,  4, 32, 17, 21, 45,  4, 32, 17, 21, 45,  4, 32,
         17, 21, 45,  4, 32, 17, 21, 45,  4, 32, 17, 21, 45,  4, 32, 17, 21, 45,
          4, 32, 17, 21, 45,  4, 32, 17, 31, 47,  4, 32, 17, 21, 45,  4, 32, 17,
         21, 45,  4, 32, 17, 31, 47,  4, 32, 17, 31, 47,  4, 32, 17, 31, 47,  4,
         49, 17, 21, 45,  4, 32, 17, 31, 47,  4, 32, 17, 31, 47,  4, 32, 17, 31,
         47,  4, 32, 17, 31, 47,  4, 32, 17, 31, 47,  4, 32, 17, 31, 47,  4, 32,
         17, 31, 47,  4, 32, 17, 31, 47,  4, 32, 17, 31, 47,  4, 19,  2,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
          0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0])
       


       t = SDRIdeaArray(10, 7, 0)
       t.sdr = goal

       sdr_idea_deserializer.deserialize(t)
    


if __name__ == '__main__':
    unittest.main()