import os,re,sys,shutil
#CONSTANTS
BASE_ADDRESS=os.getcwd()

UNWANTED=('.dat','.jpg','.nfo','.txt') #REMOVE THESE EXTENSIONS,ADDS YOUES HERE DONT DELETE
UNWANTED_FILENAME_ERRORCODE='removecode:191'  #DONT CHANGE THIS

WANT_NAME='([\S\s]+)[ (\[-_.][0-9][0-9][0-9][0-9][.\s\])_-]+' #GET MOVIE NAME ,DONT CHANGE THIS
WANT_DATE='[\S\s]+[ (\[-_.]([0-9][0-9][0-9][0-9])[.\s\])_-]+' #GET DATE ,DONT CHANGE THIS

UNWANTED_CRAP=[
               '[ _(\[.]*$',
               '^[\s\S]*www.*.com[-\s.]*'
              ] #REMOVE THESE FROM THE NAME,ADD REGULAR EXPRESSION HERE DONT DELETE PREVIOUS



def condenseName(movie_name):
       original=movie_name
       try: 
        base,ext=os.path.splitext(movie_name) #BASE IS MOVIE NAME AND EXT IS EXTENSION
        base=base+'.' #TOFORCE END AFTER DATE
        if ext in UNWANTED:
            return UNWANTED_FILENAME_ERRORCODE 
        temp_movie=re.findall(WANT_NAME,base) #GET MOVIE NAME
        movie_name=temp_movie[0]
        for unwanted in UNWANTED_CRAP:
            movie_name=re.sub(unwanted,'',movie_name)
        temp_date=re.findall(WANT_DATE,base) #GET DATE
        temp_date[0]='('+temp_date[0]+')' 
        movie_name=movie_name+' '+temp_date[0]
        movie_name=movie_name.replace('.',' ')
        movie_name=movie_name.replace('-',' ')
        movie_name=movie_name.replace('_',' ')
        return movie_name+ext
       except:
        return original



#SEACRCH FOR FILES IN CURRENT DIRECTORY AND RETURN FOLDER_URL AND FILE NAMES    
def get_files(url):
  os.chdir(url)
  files=os.listdir(url)
  movies=list()
  folders=list()
  for each_file in files:
      if os.path.isfile(each_file):
          movies.append(each_file)
      if os.path.isdir(each_file):
          folders.append(each_file)
  folder_url=[]
  for folder in folders:
       path=url+'\\'+folder
       folder_url.append(path)
  return folder_url,movies



#CUSTOM ERROR HANDLER
def handle_error(ERROR,movie,new_movie):
              print()
              exp=''
              for i in range(10):exp+=('*')
              exp+=ERROR
              for i in range(10):exp+=('*')
              print(exp)
              
              sys.stdout.write(movie+'----------->')
              sys.stdout.write (new_movie)
              print()
              for i in range(len(exp)):sys.stdout.write('*')
             


#RENAME\SEARCH\COPY TO BASE VARIOUS FILES IN FOLDER    
all_folders=list()
all_folders.append(BASE_ADDRESS)
file=open('log.txt','a+')
log=file.read() 
file.close()
def main():
    global log
    while len(all_folders):
          address=all_folders.pop()
          url,movies=get_files(address)
          for movie in movies:
              new_movie_names=list()
              new_movie_names.append(condenseName(movie))
                                          
              # REMOVING UNWANTED FILES    
              if new_movie_names[0] == UNWANTED_FILENAME_ERRORCODE:
                    os.remove(movie)
              else:
                    if new_movie_names[0] == movie:
                          handle_error('NAME NOT CHANGED!',movie,new_movie_names[0])   #ERROR
                   
                   
                    # IF STATEMENT FOR RENAME
                    if new_movie_names[0] not in os.listdir(os.curdir):
                          print 
                          sys.stdout.write(movie+'----------->')
                          sys.stdout.write (new_movie_names[0])
                          os.rename(movie,new_movie_names[0]) #RENAME 
                          log+=movie+"|"+new_movie_names[0]+"\n"
                    #ERROR HANDLING
                    else:
                           if movie != new_movie_names[0]:
                             handle_error('NAME CLASH ERROR!',movie,new_movie_names[0])  #ERROR
                    # IF STATEMENT FOR RENAME ENDED
  
                   
                    #COPYING TO BASE
                    #MAIN OPERTIONS
                    if new_movie_names[0] not in os.listdir(BASE_ADDRESS):
                          shutil.move(new_movie_names[0],BASE_ADDRESS)
                    #ERROR HANDLING
                    else:
                          if new_movie_names[0] != movie:
                            handle_error('DUBLICATE FILE',movie,new_movie_names[0])   #ERROR
                    #ENDING COPYING TO BASE DONE 

          for folder_url in url:
              if folder_url not in all_folders:
                  all_folders.append(folder_url)
          print('\n-------------------------------------------------------------------------\n')
  


#DELETING FOLDERS\CHECKING FOR FOLDERS
def clear():
  os.chdir(BASE_ADDRESS)
  files=os.listdir(BASE_ADDRESS)
  movies=list()
  folders=list()
  for each_file in files:
      if os.path.isdir(each_file):
          folders.append(each_file)
  if len(folders)==0:
    print('Every thing is good!')
    return
  print('Preparing to remove:' +str(folders))
  choice=input('Enter YES to remove:')
  if choice.lower()!='yes':
    return 
  for folder in folders:
    sys.stdout.write('Removing '+folder)
    shutil.rmtree(folder)
    print('\n'+folder+'  --Removed')


#-------------------------------------END OF FUNCTIONS-----------------------------------------------------

  
if __name__=="__main__":
   main()
   clear()
   input('Enter to exit!')
   file=open('log.txt','a+')     
   file.write(log)
   file.close()
   exit()
