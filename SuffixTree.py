# python3
"""
Constructing Suffix Tree: Linear-Time Algorithm

• Suffix trees enable fast Exact Multiple Pattern
Matching:
   • Runtime: O(|Text| + |Patterns|)
   • Memory: O(|Text|)

Constructing Suffix Tree: Naive Approach
• Quadratic runtime:
– O(|Text|)^2
"""


class TreeNode:

    # creates a node for inserting into the suffix Tree
    def __init__(self, pos=None, length=None):
        self.start_pos = pos
        self.length = length
        self.children = []
        self.parent = None

    # adds the child node to the parent Node
    def add_child(self, child):
        child.parent = self
        self.children.append(child)


class Tree:

    # stores the head (root) for the suffix Tree
    def __init__(self, head):
        self.head = head

    # This function takes the full text and then converts it in to a Suffix Tree
    def create_tree(self, text):
        text_len = len(text)  # stores the length of the Text
        flag1=True
        i = 0  # stores the index of the Text
        while i < text_len:
            flag = True  # used to find weather the substring allready exists in the Sffix Tree
            flag1 = True  # stores the while looping condition
            temp1 = self.head
            s_pos = i # stores the starting position of the current substring
            n = 0

            # A LOOP that returns the node where the New subText should be added
            while flag1:

                if len(temp1.children) > 1 or temp1 == self.head:
                    """
                    if the children are greater than 1 ,because last Node(That stores actual text info) should contain 
                    atleast one node that stores the starting position of the SubText 
                    """

                    for j in temp1.children:

                        n1 = 0  # stores the How many characters found in temp1 Node that belongs to the current Subtext
                        if text[s_pos] == text[j.start_pos]:

                            # catches the node where the contains the starting postion
                            temp1 = j

                            if temp1.start_pos + temp1.length >= text_len:  # take cares the error (index out of range)
                                l = text_len
                            else:
                                l = temp1.start_pos + temp1.length

                            for k in range(temp1.start_pos, l):
                                if text[s_pos + n1] == text[k]:
                                    n1 += 1  # one character is matching with the node text
                                    if s_pos + n1 >= text_len or k + 1 >= text_len:  # error (index out of range)
                                        break
                                else:
                                    break

                            if s_pos + n1 == text_len:
                                """
                                CASE : 1
                                If all the subtext characters are found allready in the Tree ,and Ended in the current
                                temp1 Node.
                                """
                                flag = True
                                n = n1  # stores the no.of charachters found in that perticular node
                                flag1 = False  # stopes while loop

                                break

                            elif n1 < temp1.length:
                                """
                                CASE : 2
                                If all the subText characters are not found in the tree and found characters till current
                                temp1 Node(only a part of it are matched)
                                them it goes and creates a New node for the rest of the subtext and divides the temp1 
                                till the matched characters(n1 ).
                                """
                                flag = False
                                s_pos = s_pos+n1
                                """
                                Now staring position is changed to s_pos+n1 so that from next while iteration 
                                it starts checking from the part of the substring that  is not found in that Node
                                """

                                n = n1
                                flag1 = False

                                break

                            else:
                                """
                                CASE : 3
                                If the temp1 length has exceeded and all the elements of subtext are note found then
                                it again goes to the recursive function witch checks for the rest Subtext  
                                """
                                s_pos = s_pos+n1
                                n = n1

                                flag1 = True
                                break

                        else:
                            flag = False
                            flag1 = False

                    else:
                        flag = False
                        flag1 = False
                        break

                else:

                    flag = False
                    break




            temp = temp1

            if flag:
                if n < temp.length:
                    """
                     if the text is found as a part of the temp Node text
                     then it separates the node till similar characters and then adds a child node to temp node that stores 
                     the starting position of the current subtext( i ) 
                    """

                    node = TreeNode(temp.start_pos+n, temp.length-n)
                    node.children = temp.children
                    temp.children = []
                    temp.add_child(node)
                    temp.length = n

                    node1 = TreeNode('$', i)  # node that stores the starting position
                    temp.add_child(node1)

                else:
                    """
                     if all subtext is found in the temp Node text
                     then it just adds a child node to temp node that stores 
                     the starting position of the current subtext( i ) 
                    """

                    node1 = TreeNode('$', i)
                    temp.add_child(node1)

                i += 1
            else:

                if n > 0 and n != temp.length:

                    # crates a new node for storing the rest of the text that is being divided from its parent(temp noe)
                    node = TreeNode(temp.start_pos + n, temp.length - n)
                    node.children = temp.children
                    temp.children = []
                    temp.add_child(node)

                    # changes the length of the temp , since it is divided
                    temp.length = n

                    # crates a new node for storing the rest of the subtext

                    node = TreeNode(s_pos, text_len - s_pos)
                    temp.add_child(node)

                    # node that stores the starting position
                    node1 = TreeNode('$', i)
                    node.add_child(node1)

                    i += 1

                else:
                    """
                    creates a new node for entire subText since the starting pos of the subText is not found in the Tree
                    """
                    node = TreeNode(s_pos, text_len - s_pos)
                    temp.add_child(node)
                    node1 = TreeNode('$', i)
                    node.add_child(node1)
                    i += 1



    def search_text(self,text,pattern):

        temp = self.head
        i = 0
        flag = False
        while i < len(pattern):

            for child in temp.children:

                if child.start_pos != '$':
                    if pattern[i] == text[child.start_pos]:
                        temp = child

                        for j in range(temp.start_pos, (temp.start_pos + temp.length)):
                            if pattern[i] == text[j]:
                                i += 1
                            else:
                                flag = True
                                break
                            if i >= len(pattern):
                                break

                        break


            else:
                flag = True
                break

            if flag:
                break

        if i < len(pattern):
            return []


        l = []
        stack = [item for item in temp.children]

        while len(stack):

            child = stack[0]
            if child.start_pos == '$':
                l.append(child.length)
                del stack[0]
            else:
                [stack.append(item) for item in child.children]
                del stack[0]

        return l

    def tree_print(self, parent, text, n):
        for child in parent.children:
            if child.start_pos == '$':
                print(' : ', child.length, end='')
        else:
            print()

        for child in parent.children:

            if child.start_pos == '$':
                pass
            else:

                print(n, end='')
                print(n * '--', end=' ')

                for j in range(child.start_pos, (child.length + child.start_pos)):
                    print(text[j], end='')

            if len(child.children):
                self.tree_print(child, text, n+1)


if __name__ == '__main__':
    s = input()

    str_list = [item for item in s]

    root = TreeNode('root', 'root')
    root.count = 0
    tree = Tree(root)
    tree.create_tree(str_list)
    #print(len(s))

    tree.tree_print(root, str_list, 1)

    n = int(input())
    found_list = []

    for i in range(n):
        s = input()
        if (len(s) <= len(str_list)):
            l = tree.search_text(str_list, s)
            [found_list.append(j) for j in l]

    found_list.sort()
    for i in found_list:
        print(i,end=' ')









