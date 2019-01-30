# coding: utf-8
""" copyright© 2019 — Luc Bertin - License MIT """

from tkinter import *
from Twitter_Class_Analysis import Twitter_Analysis
from Linkedin_Companies_scrapping import LinkedIn_Analysis


analysisLkdIn = LinkedIn_Analysis()

# FRONT
def action_on_button1():
    display_message.config(text = str(Twitter_Analysis.authentificator()))

def action_on_button2():
    dico = str(dico_entry.get())
    filename = str(filename_entry.get())
    max_tweets = int(str(maxtweets_entry.get()))
    CSV_LinkedIn = str(companiesLinkedInfile_entry.get())
    company_name = str(company_entry.get())
    
    print('Entreprise renseignee : ' + company_name)
    print('CSV renseigne : ' + CSV_LinkedIn )
    
    analysis = Twitter_Analysis(dico_file=dico,filename=filename,
                                maxTweets=max_tweets, company_name=company_name,
                                companies_CSV_file=CSV_LinkedIn)
    
    print('\nListe des companies : '+str(analysis.companies_list)+'\n')
    print('\nRequete Finale : '+ str(analysis.searchQuery))
    
    analysis.search()
    display_message.config(text = "Fini!")

def action_on_button3():
    dico = str(dico_entry.get())
    filename = str(filename_entry.get())
    max_tweets = int(str(maxtweets_entry.get()))
    analysis = Twitter_Analysis(dico_file=dico, filename=filename,
                                maxTweets=max_tweets, company_name=company_entry.get(),
                                companies_CSV_file=companiesLinkedInfile_entry.get())
    analysis.tweets_to_dataframe()
    display_message.config(text = "Dataframe disponible !")

def action_on_button4():
    global analysisLkdIn
    if analysisLkdIn.STOP_EXECUTION==0:
        keyword = str(LinkedInKeyword_entry.get())
        output_filename = "LinkedInCompanies"+str(filename_entry.get())+".csv"
        analysisLkdIn.keyword = keyword
        analysisLkdIn.output_filename = output_filename
        analysisLkdIn.start()
        analysisLkdIn.STOP_EXECUTION=1
    elif analysisLkdIn.STOP_EXECUTION==1:
        analysisLkdIn.STOP_EXECUTION = 2
        print('finish1')
        analysisLkdIn.join()
        print('finish2')
        analysisLkdIn = LinkedIn_Analysis()
        display_message.config(text = "execution stopped !")


root = Tk()
root.title('PI2 Project — Twitter Analysis')
root.geometry('{}x{}'.format(350, 500))
root.update()
root.minsize(root.winfo_width(), root.winfo_height())

dico_label = Label(root, text='Nom du fichier dico de valeurs :')
dico_entry = Entry(root, background="lavender")
companiesLinkedInfile_label = Label(root, text='Nom du CSV LinkedIn :')
companiesLinkedInfile_entry = Entry(root, background="lavender")
filename_label = Label(root, text='Nom du fichier de sortie :')
filename_entry = Entry(root, background="lavender")
maxtweets_label = Label(root, text='Nb Maximum de tweets :')
maxtweets_entry = Entry(root, background="lavender")
company_filter = Label(root, text='Une entreprise en particulier ?')
company_entry = Entry(root, background="lavender")
display_message = Label(root, text='')


authentification_button = Button(root, text='Authentifiate!', width=25, command=action_on_button1)
tweeterJson_button = Button(root, text='JSON', width=25, command=action_on_button2)
tweeterCSV_button = Button(root, text='CSV', width=25, command=action_on_button3)


LinkedInKeyword_label = Label(root, text='Pas de CSV d\'entreprise?\n Quel Keyword d\'entreprise :')
LinkedInKeyword_entry = Entry(root, background="bisque")
LindedIn_ico = PhotoImage(file="linkedin-3-32.gif")
LinkedIn_button = Button(root, image=LindedIn_ico, command=action_on_button4)


## Default values
dico_entry.insert(END, 'dico_file.txt')
companiesLinkedInfile_entry.insert(END, 'LinkedInCompanies.csv')
filename_entry.insert(END, 'tweets')
maxtweets_entry.insert(END, '200')
company_entry.insert(END, 'Nike')
LinkedInKeyword_entry.insert(END, 'environnement')



dico_label.pack()
dico_entry.pack()
companiesLinkedInfile_label.pack()
companiesLinkedInfile_entry.pack()
filename_label.pack()
filename_entry.pack()
maxtweets_label.pack()
maxtweets_entry.pack()
company_filter.pack()
company_entry.pack()
authentification_button.pack()
tweeterJson_button.pack()
tweeterCSV_button.pack()
display_message.pack()

LinkedInKeyword_label.pack()
LinkedInKeyword_entry.pack()
LinkedIn_button.pack()

root.mainloop()
