from myfolder import folder
from output_scorer import score_output
import os
import shutil
import sys

local_folder = "./" + folder
main_outputs = "./outputs"
main_inputs = "./inputs"

def main(folder):
    old_scores, new_scores = 0, 0
    print_results = False
    #Iterate through small, medium, large
    for size_category in os.listdir(folder):
        #For each output in folder:
        outputs = os.listdir(folder + "/" + size_category)
        if len(outputs) == 0:
            print("No files to merge in {}.".format(size_category))
        else:
            print("Merging files in {}...".format(size_category))
            print_results = True

        for output in outputs:
            
            outputfoldername = main_outputs + "/" + size_category + "/" + output 
            localoutputname = folder + "/" + size_category + "/" + output
            inputfoldername = main_inputs + "/" + size_category + "/" + output[:-4]
            #Check if exists in main_outputs/folder
            if (os.path.isfile(outputfoldername)):
                prev_score = 1 - score_output(inputfoldername, outputfoldername)[0]
            else:
                prev_score = 1
            
            
            #If exists, run score comparison, overwrite if better score
            new_score = 1 - score_output(inputfoldername, localoutputname)[0]
            prev_score = prev_score if prev_score > 0 else 0.000000001
            old_scores += prev_score
            new_scores += new_score
            improvement = ((prev_score - new_score)/prev_score)*100

            print("[GRAPH {}]".format(output[:-4]).ljust(14) + "Old score: {0:.2f}".format(prev_score).ljust(19) + "|".ljust(3) + "New score: {0:.2f}".format(new_score).ljust(19) + "|".ljust(3) + "Improvement: {0:.2f}%".format(improvement).ljust(15))
            if improvement > 0:
                shutil.move(localoutputname, outputfoldername)
            else:
                #Delete from folder
                os.remove(localoutputname)
                
    if print_results:
        #Print batch improvement
        old_scores = old_scores if old_scores > 0 else 0.00000001
        print("-"*80)
        print("Total improvement this batch: {0:.2f}%".format(((old_scores - new_scores)/old_scores)*100))
        print("-"*80)

def run_all():
    for f in ["gabby", "ian", "dustyn"]:
        main("./" + f)

if __name__ == '__main__':
    len_args = len(sys.argv)
    if len_args == 1:
        main(local_folder)
    elif len_args == 2:
        if sys.argv[1] == "self":
            main(local_folder)
        elif sys.argv[1] == "all":
            run_all()
        else:
            raise ValueError("Incorrect input format")