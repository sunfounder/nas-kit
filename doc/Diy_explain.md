# This document is used to illustrate how to add your own interface page and menu option.
# 1.Add Menu column options 
```
# Menu diy example
### declares a menu option called "shutdown",the left button is named as "no", the right one as "yes".
item_1 = Menu_item_templates(item_name = "shutdown",choise_button_one = "NO",choice_button_two = "YES") 

# python
##python_cmd is to execute the python statement,input_cmd_2 corresponds to the above choice_button_two
item_1.python_cmd(input_cmd_2 ="page.shutdown_Animation()") 

# linux
##python_cmd is used to execute the linux command,input_cmd_2 corresponds to the above choice_button_two
item_1.linux_cmd(input_cmd_2 ="sudo poweroff") 
```
## Instruction: item_1 stands for the first menu option, and the naming format is "item_" + "num"; num must be counted in order. Then add the new objects into Menu_item_dict = {1:item_1.item_name, 2:item_2.item_name, 3:item_3.item_name, 4:item_4.item_name} such as 5:item_5.item_name.(This dict is on the line 247 in the raspi_omv_main.py).finally,need to reboot

# 2.Add Page
## Add Page Instruction: Examples: the page_1_setup in class Page is used to draw the invariable images; on the contrary, page_1_update is used to draw the ever-changing images. They both use self.draw to draw images and __call__ to show, so you only need add new functions to class Page of page files, for example, you can create your own pages via "page_4_setup and page_4_setup". Then change the page_length of raspi_omv_main.py to the current page number. 