'''
Created on Apr 24, 2017

@author: aneesh.c
'''

# welcome_note = [['Hi, I am GunBro, a Chatbot. I can help you with all your firearms needs, How may \
# I help you today?'], ['I can make recommendation if you tell me your use for the \
# firearm. What is your interest?'], ['Welcome to Gunbro. May I help you find a firearm \
# or an accessory today?']]

welcome_note = [['Hi, I am Joe, a Chatbot, I can make a \
recommendation if you tell me how you plan to use the \
firearm, or provide a specific use such as hunting \
or personal protection or target shooting for example']]



type_of_shooting = ["What's the type of target you want to shoot?"]
type_of_shooting_prepper = ['Oh, you are preparing for an attack,']
type_of_shooting_prepper_category = ['Are you searching guns for Defense or survival?']
prepper_objects = ['Defense', 'Survival']

personal_protection_text = ['Do you prefer a gun for concealed carry or for use \
in the home where small size and light weight are not as important?']
# personal_protection_text2 = ['Or do you want to use it while travelling']


collector_text = ['Oh you are a gun collector']
collector_text2 = ['What types of guns you want to look into?']
collector_text3 = ['We have a good collection of Vintage Firearms, Commemorative firearms, and military used guns']
collector_objects = ['Commemorative/Special Issue/Limited Production', 'Military Issue/Use', 'Vintage Firearms']

hunter_text = ['Oh, you are going hunting.']
hunter_text2 = ['What are you hunting?']
hunter_text3 = ['For example, are you going hunting for \
rabbit/squirrel/gamebirds/waterfowl/ducks/deer/hogs/elk/antelope/dove/bear/etc?']

objects = ["Which one do you prefer? Paper targets or metallic targets, round ring targets, clay targets or bowling pins ?"]
target_lists = ['metallic targets', 'round ring targets', 'clay targets' , 'bowling pins']

first_end_note = ['Results shown are best suited for']
end_note = ['Please look at the search results I could gather ']

targets_guns = {'paper targets':'Benchrest, Bullseye',\
                'metallic targets':'Metallic Silhouette, Cowboy Action Shooting, Infor\
mal Recreation Shooting, Black Powder Shooting, International Position Shooting, Practical/Combat-Type Shooting, \
Single-shot Target Shooting',
                'clay targets':'Clay Shooting',
                'round ring targets':'International Position Shooting',
                'bowling pin':'Bowling Pin',
                'other':'Informal Recreation Shooting',
                 'Black Powder Shooting':'Black Powder Shooting',
                 'Benchrest' : 'Benchrest',
                 'Cowboy Action Shooting': 'Cowboy Action Shooting',
                 'Informal Recreation Shooting': 'Informal Recreation Shooting',
                 'International Position Shooting':'International Position Shooting',
                 'Practical/Combat-Type Shooting':'Practical/Combat-Type Shooting',
                 'Single-shot Target Shooting':'Single-shot Target Shooting'}

military = ['Which one do you prefer? Close contact (<100 yards) guns or Distant Contact (>100 yards) guns ?']
military_second = [' are one of the best choices for military operations']
military_objects = ['Close contact (<100 yards)', 'Distant Contact (>100 yards)']


sporting_arms = ['We have a good collection of sporing arms which inludes AK style guns, AR style guns and other sporting rifles.']
sporting_arms2 = ['Which category you would preffer?']
sporting_objects = ['AK Style', 'AR Style', 'Other Sporting Rifles']

second_level_text = ['I can again narrow down the recommendation further, Do you want to proceed?']

unknown_input = ["Sorry I didn't get you"]

host_inventory = 'gunbrodb.gogocar.com'
user_inventory = 'gunbro_kapow'
passwd_inventory = 'tRbfgG4Qu1bQmvH'
db_inventory ='gun_bro'
no_recommendation = ['No matches found']

manufacturers = ['Savage', 'Beretta', 'Winchester', 'Davey Crickett', 'Bersa', 'KEL-TEC', '\
H&R 1871', 'Taurus', 'Bond Arms', 'Springfield', 'EAA Corp.', 'Glock', 'Smith & Wesson\
', 'Armalite', 'Del-Ton', 'Rock River Arms', 'Henry Repeating Arms', '\
American Tactical', 'Weatherby', 'Diamondback Firearms', '\
Heckler & Koch', 'Kimber', 'Sig Sauer', 'Browning', '\
Marlin', 'Zastava Arms', 'FN America', 'Howa', 'Kahr Arms', '\
Daniel Defense', 'Hi Point Firearms', 'DPMS', 'Ruger', 'Walther', '\
Austrian Sporting Arms', 'Sako', 'Mossberg', 'Magnum Research', '\
Benelli', 'Century', 'Heritage Arms', 'Colt', 'Romarm/Cugir', '\
Remington', 'Charter Arms', 'Canik', 'Bushmaster', 'CZ-USA']