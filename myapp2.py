# coding: utf-8

from tkinter import *
from Twitter_Class_Analysis import Twitter_Analysis

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

root = Tk()
root.title('PI2 Project — Twitter Analysis')
root.geometry('{}x{}'.format(350, 400))
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



## Default values
dico_entry.insert(END, 'dico_file.txt')
companiesLinkedInfile_entry.insert(END, 'LinkedInCompanies.csv')
filename_entry.insert(END, 'tweets')
maxtweets_entry.insert(END, '200')
company_entry.insert(END, 'Nike')



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


root.mainloop()
