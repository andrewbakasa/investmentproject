
function getDateTime_(inputdate){
    //April 26, 2022, 12:53 p.m.
    return  getfullMonthOfYear(inputdate)+ ' '  + inputdate.getDate() + 
             ', ' +  inputdate.getFullYear()+ ', ' +  padZero(inputdate.getHours()) +':' +  padZero(inputdate.getMinutes())
}
function getfullDateTime_(inputdate){
    //Sun 22 May 2022 20:05:17
    return  getshortDayOfWeek(inputdate) + ' ' + inputdate.getDate() + ' '  + getfullMonthOfYear(inputdate)+ ' '   + 
             ', ' +  inputdate.getFullYear()+ ', ' +  padZero(inputdate.getHours()) +':' + 
              padZero(inputdate.getMinutes())+':' +  padZero(inputdate.getSeconds())
}

function padZero(input){
    //console.log(typeof(input))
    if ((input) < 10){
        return '0' + input
    }else {
        return input
    }
}

function getshortDate_(inputdate){
    //Aug 12. 2022
    return getshortMonthOfYear(inputdate) + ". "  + inputdate.getDate() + ", "  +  inputdate.getFullYear()
}

function getmediumDate_(inputdate){
    //Fri 12 Aug 2022
    return getshortDayOfWeek() + ' '  + inputdate.getDate() + ' ' + getshortMonthOfYear(inputdate) + " "  +  inputdate.getFullYear()
}

function getfullDate_(inputdate){
    //Friday 12 August 2022
    return getfullDayOfWeek() + ' '  + inputdate.getDate() + ' ' + getfullMonthOfYear(inputdate) + " "  +  inputdate.getFullYear()
}
 function getDay(inputdate){
    return inputdate.getDay()   
 }
 function getfullMonthOfYear(inputdate){
     var  month_var
    //  new Date().getHours
    //  new Date().getMinutes
    //  new Date().getSeconds
     //new Date().getTime()
     // new Date().getFullYear()
     // new Date().getMonth()
     // new Date().getUTCDay()
     // new Date().getDate()
     // new Date().getDay()
     switch (inputdate.getMonth()) {
             case 0:
             month_var = "January";
             break;
             case 1:
             month_var = "February";
             break;
             case 2:
             month_var = "March";
             break;
             case 3:
             month_var = "April";
             break;
             case 4:
             month_var = "May";
             break;
             case 5:
             month_var = "June";
             break;
             case 6:
             month_var = "July";
             break;
             case 7:
             month_var = "August";
             break;
             case 8:
             month_var = "September";
             break;
             case 9:
             month_var = "October";
             break;
             case 10:
             month_var = "November";
             break;
             case 11:
             month_var = "December"; 
             break;                   
             default:
             month_var = "January";
          
     }
     return month_var
 }
 function getshortMonthOfYear(inputdate){
    var  month_var
    // new Date().getFullYear()
    // new Date().getMonth()
    // new Date().getUTCDay()
    // new Date().getDate()
    // new Date().getDay()
    switch (inputdate.getMonth()) {
            case 0:
            month_var = "Jan";
            break;
            case 1:
            month_var = "Feb";
            break;
            case 2:
            month_var = "Mar";
            break;
            case 3:
            month_var = "Apr";
            break;
            case 4:
            month_var = "May";
            break;
            case 5:
            month_var = "Jun";
            break;
            case 6:
            month_var = "July";
            break;
            case 7:
            month_var = "Aug";
            break;
            case 8:
            month_var = "Sep";
            break;
            case 9:
            month_var = "Oct";
            break;
            case 10:
            month_var = "Nov";
            break;
            case 11:
            month_var = "Dec"; 
            break;                   
            default:
            month_var = "Jan";
         
    }
    return month_var
}
 function getfullDayOfWeek(inputdate){
     var  weekday
     // new Date().getFullYear()
     // new Date().getMonth()
     // new Date().getUTCDay()
     // new Date().getDate()
     // new Date().getDay()
     switch (inputdate.getDay()) {
             case 0:
             weekday = "Sunday";
             break;
             case 1:
             weekday = "Monday";
             break;
             case 2:
             weekday = "Tuesday";
             break;
             case 3:
             weekday = "Wednesday";
             break;
             case 4:
             weekday = "Thursday";
             break;
             case 5:
             weekday = "Friday";
             break;
             case 6:
             weekday = "Saturday";
             break;
             default:
             weekday = "";
          
     }
     return weekday
 }

 function getshortDayOfWeek(inputdate){
    var  weekday
    // new Date().getFullYear()
    // new Date().getMonth()
    // new Date().getUTCDay()
    // new Date().getDate()
    // new Date().getDay()
    switch (inputdate.getDay()) {
            case 0:
            weekday = "Sun";
            break;
            case 1:
            weekday = "Mon";
            break;
            case 2:
            weekday = "Tue";
            break;
            case 3:
            weekday = "Wed";
            break;
            case 4:
            weekday = "Thur";
            break;
            case 5:
            weekday = "Fri";
            break;
            case 6:
            weekday = "Sat";
            break;
            default:
            weekday = "";
         
    }
    return weekday
}

