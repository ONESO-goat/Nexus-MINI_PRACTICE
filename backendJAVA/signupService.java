package backend_java;

public class signupService {
  public static void main(String args[]){
    
}

public boolean validateUsername(String username){
  
    if(username == null ||  username.isEmpty()){
      return false;
    }
    
    username = username.toLowerCase();

    if(username.length() > 14 || username.length() < 3){
      return false;
    }

    if(usernameIsDigit(username) == true){
      return false;
    }
    return true;
  }


  // Check if username is number only
  public boolean usernameIsDigit(String username){
    try{
      Integer.parseInt(username);
      return true;
    } catch(NumberFormatException e){
      return false;
    }
  }

  //Validate the password
  public boolean validatePassword(String password){
    
    if(password == null || password.isEmpty()){
      return false;
    }

    if(password.toLowerCase().length() < 8 || password.toLowerCase().length() > 120){
      return false;
    }
    if(wordsInsidePassword(password) == false){
      return false;
    }

    return true;
  }
  // Check the letters inside password for special characters, characters, and digits
  public boolean wordsInsidePassword(String password){
    if(password == null || password.isEmpty()){
      return false;
    }
    boolean hasChar = false;
    boolean hasDigit = false;
    boolean hasSpec = false;

    for(char c: password.toCharArray()){
      if(Character.isDigit(c)){
        hasDigit = true;
      }
      else if(Character.isLetter(c)){
        hasChar = true;
      }
      else{
        hasSpec = true;
      }
    }
    return hasChar && hasDigit && hasSpec;
  }
}
