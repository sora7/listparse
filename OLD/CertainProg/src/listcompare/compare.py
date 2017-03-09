# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__="alex"
__date__ ="$27.07.2014 17:04:17$"

class ListCompare(object):

# #    todo
# #    some cute methods like:
# #    union(list1).union(list2).union(list3).diff(list4).inter(list5)
    
    def add(self, initial_list):
        pass

    @staticmethod
    def mk_store(lists):
        # make dict (item.ani_id, item)
        pass

    @staticmethod
    def inter(lists):
        if len(lists) < 2:
            raise ValueError('must be >1 lists')
        
        lst = lists[0]
        store = dict(
                     (item.ani_id, item) for item in lst 
                     )
        inter = set([i.ani_id for i in lst])
        
        for lst in lists[1:]:
            inter = inter.intersection(set([item.ani_id for item in lst]))
            for item in lst:
                store[item.ani_id] = item
            
        output = []
        for item in inter:
            output.append(store[item])
        
        return output

    @staticmethod
    def diff(lists):
        # titles are in first list, but not in second
        if len(lists) != 2:
            raise ValueError('must be 2 lists')

        list1_set = set([item.ani_id for item in lists[0]])
        list2_set = set([item.ani_id for item in lists[1]])
        differ = list1_set.difference(list2_set)
        
        output = []
        for item in lists[0]:
            if item.ani_id in differ:
                output.append(item)
                
        return output

    @staticmethod
    def union(lists):
        res = []
        for lst in lists:
            for item in lst:
                res.append(item)
        return res

if __name__ == "__main__":
    print "Hello World"
