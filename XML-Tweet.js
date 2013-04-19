//Created By @Orymeyer
function init(){
  
  twttr_init();
  _db();
  fetch();
  
  
   var feed = "XXXXX" //XML feed Source
   ScriptProperties.setProperty("feed", feed)
  
}

function fetch() {
  //Fetch the latest feed
  var text = UrlFetchApp.fetch("feed").getContentText();
  var doc = Xml.parse(text);
  //Channel,Items,Description are Elements of the feed.Can Be Replaced.
  var items = doc.getElement().getElement("channel").getElements("item");
  var current  = items[0].getElement("description").getText();
  
  
  Logger.log(current);
  
  var last = read_db();
  
  var code = check(current,last);
 
 
  
  if(code==1)
  {
    
    //Update the Database with the Latest Retrieved Feed
    update(current);
    Logger.log("Database Updated!"); 
    
    if(current.length<=140){
     post(current);
    }
    
    else
    {
      
   //if number of characters are greater than 160,split them into two parts and post them/
   Split(current);
   
    
    }
  }
  
  
}

function _db() {
  
  
  //Initialises the database.Must be run once at the beginning
  var db = ScriptDb.getMyDb();
  var  ob = {status:"Initialising Bot..."};
  var saved = db.save(ob);
  var _id = saved.getId();
  ScriptProperties.setProperty("ID", _id);
  
  
 }

function read_db(){
  
  //Reads the DB for the last stored Feed
  var db = ScriptDb.getMyDb();
  var loaded = db.load(ScriptProperties.getProperty("ID"));
  return loaded.status;
}

function update(updte){
  
  //Updates the DB with the provided string
  var db = ScriptDb.getMyDb();
  var loaded = db.load(ScriptProperties.getProperty("ID"));
  loaded.status = updte;
  
 var saved = db.save(loaded);
  var _id = saved.getId();
  
 ScriptProperties.setProperty("ID", _id); 
}


function check(now,then){
  //Checks if the Database is upto date.Compares the retrieved feed with the feed in Database.
  if(now==then){
    Logger.log("Database is upto date");
   return 0;
  }
  else{
    Logger.log("Update Required!");
    return 1;
  }
}

function twttr_init(){
  //Initialises Twitter.Must be Run Once.
  var TWITTER_CONSUMER_KEY     = "XXXXXX";  
  var TWITTER_CONSUMER_SECRET  = "XXXXXX";  //Replace all the XXXXX dummy values
  var TWITTER_HANDLE           = "XXXXXXX";   
  
 
  
  
  ScriptProperties.setProperty("CONSUMER_KEY",     TWITTER_CONSUMER_KEY);
  ScriptProperties.setProperty("CONSUMER_SECRET",  TWITTER_CONSUMER_SECRET);
  ScriptProperties.setProperty("TWITTER_HANDLE",   TWITTER_HANDLE);
  
  oAuth();
  
}


function post(tweet){
   
  //Function for Postng tweet.
  oAuth();
   var options =
  {
    "method": "POST",
    "oAuthServiceName":"twitter",
    "oAuthUseToken":"always"    
  };
  
  var status = "https://api.twitter.com/1.1/statuses/update.json";
  
  status = status + "?status=" + encodeString(tweet);
  
  
  try {
    var result = UrlFetchApp.fetch(status, options);
  
  }  
  catch (e) {
    Logger.log(e.toString());
  }  
}
  
  


function oAuth() {
 
  var oauthConfig = UrlFetchApp.addOAuthService("twitter");
  oauthConfig.setAccessTokenUrl("https://api.twitter.com/oauth/access_token");
  oauthConfig.setRequestTokenUrl("https://api.twitter.com/oauth/request_token");
  oauthConfig.setAuthorizationUrl("https://api.twitter.com/oauth/authorize");
  oauthConfig.setConsumerKey(ScriptProperties.getProperty("CONSUMER_KEY"));
  oauthConfig.setConsumerSecret(ScriptProperties.getProperty("CONSUMER_SECRET"));
 
}



  
 function encodeString (q) {
   var str =  encodeURIComponent(q);
   str = str.replace(/!/g,'%21');
   str = str.replace(/\*/g,'%2A');
   str = str.replace(/\(/g,'%28');
   str = str.replace(/\)/g,'%29');
   str = str.replace(/'/g,'%27');
   return str;
}
 
  function Split(String) {
    //Splits String which have more than 140 charactera into two parts.
  var one = String.slice(0,135);
  var two = String.slice(136,String.length)
  //Logger.log(one+two);
  one = "[2/2]" +one;
  two = "[1/2]"+ two;
  
  post(two);
  post(one);
   Logger.log("Successfully Splitted and posted");
  }

  
