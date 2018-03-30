# Parse jsons of 'formy zmin' and save separate tables with general_info, income, estate, 
# transport, securities, corporate rights, movables, non material assets

library(rjson)
library(data.table)

# Reading data from JSON file
# To create json file with formy zmin which match some conditions, look here: 
# https://github.com/pro100olga/declarations/blob/master/getting_data/import_formy_zmin_2018.py

decl_raw <- rjson::fromJSON(file="feed18.json")

# # Define datasets -------------------------------------------------------

general_info <- data.table(FIO = character(), office = character(), position = character(),
                           created_date = character(), url = character())

income <- data.table(url = character(),
                     person = character(),
                     incomeSource = character(),
                     source_citizen = character(),
                     source_ukr_person_name = character(),
                     source_ua_person_name = character(),
                     source_eng_person_name = character(),
                     source_ukr_company_name = character(),
                     source_ua_company_name = character(),
                     source_eng_company_name = character(),
                     objectType = character(),
                     otherObjectType = character(),
                     sizeIncome = character())

estate <- data.table(url = character(),
                     person = character(),
                     country = character(),
                     ua_cityType = character(),
                     objectType = character(),
                     otherObjectType = character(),
                     rights = character(),
                     totalArea = character(),
                     costDate = character(),
                     costAssessment = character(),
                     owningDate = character())

transport <- data.table(url = character(),
                        person = character(),
                        objectType = character(),
                        typeProperty = character(),
                        otherObjectType = character(),
                        owningDate = character(),
                        rights = character(),
                        brand_model = character(),
                        graduationYear = character(),
                        costLast = character(),
                        costDate = character())

securities <- data.table(url = character(),
                         person = character(),
                         typeProperty = character(),
                         subTypeProperty = character(),
                         otherObjectType = character(),
                         owningDate = character(),
                         amount = character(),
                         cost = character(),
                         costDate = character(),
                         costLast = character(),
                         emitent = character(),
                         emitent_type = character(),
                         emitent_ua_fullname = character(),
                         emitent_ukr_fullname = character(),
                         emitent_eng_fullname = character(),
                         emitent_ua_company_name = character(),
                         emitent_ukr_company_name = character(),
                         emitent_eng_company_name = character(),
                         emitent_eng_company_code = character(),
                         emitent_ua_company_code = character(),
                         rights = character())

corp_rights <- data.table(url = character(),
                          person = character(),
                          name = character(),
                          country = character(),
                          corporate_rights_company_code = character(),
                          legalForm = character(),
                          cost = character(),
                          cost_percent = character(),
                          costDate = character(),
                          owningDate = character(),
                          rights = character())

movables <- data.table(url = character(),
                       person = character(),
                       objectType = character(),
                       otherObjectType = character(),
                       dateUse = character(),
                       trademark = character(),
                       manufacturerName = character(),
                       propertyDescr = character(),
                       costDateUse = character(),
                       costLast = character(),
                       rights = character())

nma <- data.table(url = character(),
                  person = character(),
                  objectType = character(),
                  otherObjectType = character(),
                  owningDate = character(),
                  descriptionObject = character(),
                  costLast = character(),
                  costDateOrigin = character(),
                  rights = character())


# # Add data --------------------------------------------------------------

for (i in 1:length(decl_raw)) {

  # check that document was not corrected afterwards
  if ('corrected' %in% names(decl_raw[[i]]$related_entities$documents)) {
    
    if (length(decl_raw[[i]]$related_entities$documents$corrected) == 0) {
      
      # # General info----------------
      
      general_info <- rbindlist(list(general_info,
                                     list(
                                       # FIO
                                       paste0(decl_raw[[i]]$infocard$last_name, " ", 
                                              decl_raw[[i]]$infocard$first_name, " ", 
                                              decl_raw[[i]]$infocard$patronymic),
                                       # Office and position
                                       decl_raw[[i]]$infocard$office, decl_raw[[i]]$infocard$position,
                                       # Created date
                                       substr(decl_raw[[i]]$infocard$created_date,1,10),
                                       # Link
                                       decl_raw[[i]]$infocard$url)))
      
      
      # # Income ----------------------------------------------------------------
      
      if ("step_2" %in% names(decl_raw[[i]]$unified_source) && length(decl_raw[[i]]$unified_source$step_2) > 0) {
        
        for (j in 1:length(decl_raw[[i]]$unified_source$step_2)) {
          if (decl_raw[[i]]$unified_source$step_2[[j]] != "У суб'єкта декларування відсутні об'єкти для декларування в цьому розділі.")
          {
            income <- rbindlist(list(income,
                                     list(decl_raw[[i]]$infocard$url,
                                          decl_raw[[i]]$unified_source$step_2[[j]]$person,
                                          decl_raw[[i]]$unified_source$step_2[[j]]$incomeSource,
                                          decl_raw[[i]]$unified_source$step_2[[j]]$source_citizen,
                                          ifelse(is.null(decl_raw[[i]]$unified_source$step_2[[j]]$source_ukr_fullname), "",
                                                 decl_raw[[i]]$unified_source$step_2[[j]]$source_ukr_fullname),
                                          paste0(decl_raw[[i]]$unified_source$step_2[[j]]$source_ua_lastname, " ",
                                                 decl_raw[[i]]$unified_source$step_2[[j]]$source_ua_firstname, " ", 
                                                 decl_raw[[i]]$unified_source$step_2[[j]]$source_ua_middlename),
                                          ifelse(is.null(decl_raw[[i]]$unified_source$step_2[[j]]$source_eng_fullname), "",
                                                 decl_raw[[i]]$unified_source$step_2[[j]]$source_eng_fullname),
                                          ifelse(is.null(decl_raw[[i]]$unified_source$step_2[[j]]$source_ukr_company_name), "",
                                                 decl_raw[[i]]$unified_source$step_2[[j]]$source_ukr_company_name),
                                          ifelse(is.null(decl_raw[[i]]$unified_source$step_2[[j]]$source_ua_company_name), "",
                                                 decl_raw[[i]]$unified_source$step_2[[j]]$source_ua_company_name),
                                          ifelse(is.null(decl_raw[[i]]$unified_source$step_2[[j]]$source_eng_company_name), "",
                                                 decl_raw[[i]]$unified_source$step_2[[j]]$source_eng_company_name),
                                          decl_raw[[i]]$unified_source$step_2[[j]]$objectType,
                                          decl_raw[[i]]$unified_source$step_2[[j]]$otherObjectType,
                                          decl_raw[[i]]$unified_source$step_2[[j]]$sizeIncome)))
          }
        }
      }
      
      
      # # Estate ----------------------------------------------------------------
      
      if ("step_3" %in% names(decl_raw[[i]]$unified_source) && length(decl_raw[[i]]$unified_source$step_3) > 0) {
        
        for (j in 1:length(decl_raw[[i]]$unified_source$step_3)) {
          
          if (decl_raw[[i]]$unified_source$step_3[[j]] != "У суб'єкта декларування відсутні об'єкти для декларування в цьому розділі.")
          {
            rights <- ""
            
            if ("rights" %in% names(decl_raw[[i]]$unified_source$step_3[[j]]) && 
                length(decl_raw[[i]]$unified_source$step_3[[j]]$rights) > 0) {
              
              for (k in 1:length(decl_raw[[i]]$unified_source$step_3[[j]]$rights)) {
                rights <- paste0(rights, decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$seller, ": ",
                                 decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$citizen, ", ",
                                 ifelse(decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$citizen == "Громадянин України",
                                        paste0(decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$ua_lastname, " ",
                                               decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$ua_firstname, " ",
                                               decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$ua_middlename, ";"),
                                        ifelse(decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$citizen == "Іноземний громадянин", 
                                               decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$eng_fullname,
                                               ifelse(decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована в Україні", 
                                                      decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$ua_company_name,
                                                      ifelse(decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована за кордоном", 
                                                             decl_raw[[i]]$unified_source$step_3[[j]]$rights[[k]]$eng_company_name,
                                                             "?")))))
              }
            }
            
            estate <- rbindlist(list(estate,
                                     list(decl_raw[[i]]$infocard$url,
                                          decl_raw[[i]]$unified_source$step_3[[j]]$person,
                                          decl_raw[[i]]$unified_source$step_3[[j]]$country,
                                          decl_raw[[i]]$unified_source$step_3[[j]]$ua_cityType,
                                          decl_raw[[i]]$unified_source$step_3[[j]]$objectType,
                                          decl_raw[[i]]$unified_source$step_3[[j]]$otherObjectType,
                                          rights,
                                          decl_raw[[i]]$unified_source$step_3[[j]]$totalArea,
                                          decl_raw[[i]]$unified_source$step_3[[j]]$costDate,
                                          decl_raw[[i]]$unified_source$step_3[[j]]$costAssessment,
                                          decl_raw[[i]]$unified_source$step_3[[j]]$owningDate)))
            
          }
        }
      }
      
      
      # # Transport -------------------------------------------------------------
      
      if ("step_4" %in% names(decl_raw[[i]]$unified_source) && length(decl_raw[[i]]$unified_source$step_4) > 0) {
        
        for (j in 1:length(decl_raw[[i]]$unified_source$step_4)) {
          if (decl_raw[[i]]$unified_source$step_4[[j]] != "У суб'єкта декларування відсутні об'єкти для декларування в цьому розділі.")
          {
            
            
            rights <- ""
            
            if ("rights" %in% names(decl_raw[[i]]$unified_source$step_4[[j]]) && 
                length(decl_raw[[i]]$unified_source$step_4[[j]]$rights) > 0) {
              
              for (k in 1:length(decl_raw[[i]]$unified_source$step_4[[j]]$rights)) {
                rights <- paste0(rights, decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$seller, ": ",
                                 decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$citizen, ", ",
                                 ifelse(decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$citizen == "Громадянин України",
                                        paste0(decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$ua_lastname, " ",
                                               decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$ua_firstname, " ",
                                               decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$ua_middlename, ";"),
                                        ifelse(decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$citizen == "Іноземний громадянин", 
                                               decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$eng_fullname,
                                               ifelse(decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована в Україні", 
                                                      paste0(decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$ua_company_name, " ",
                                                             decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$ua_company_code),
                                                      ifelse(decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована за кордоном", 
                                                             paste0(decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$eng_company_name, ", ",
                                                                    decl_raw[[i]]$unified_source$step_4[[j]]$rights[[k]]$eng_company_code),
                                                             "?")))))
              }
            }
            
            transport <- rbindlist(list(transport,
                                        list(decl_raw[[i]]$infocard$url,
                                             decl_raw[[i]]$unified_source$step_4[[j]]$person,
                                             decl_raw[[i]]$unified_source$step_4[[j]]$objectType,
                                             decl_raw[[i]]$unified_source$step_4[[j]]$typeProperty,
                                             ifelse(is.null(decl_raw[[i]]$unified_source$step_4[[j]]$otherObjectType), "",
                                                    decl_raw[[i]]$unified_source$step_4[[j]]$otherObjectType),
                                             decl_raw[[i]]$unified_source$step_4[[j]]$owningDate,
                                             rights,
                                             paste0(decl_raw[[i]]$unified_source$step_4[[j]]$brand, " ", 
                                                    decl_raw[[i]]$unified_source$step_4[[j]]$model),
                                             decl_raw[[i]]$unified_source$step_4[[j]]$graduationYear,
                                             decl_raw[[i]]$unified_source$step_4[[j]]$costLast,
                                             decl_raw[[i]]$unified_source$step_4[[j]]$costDate)))
            
            
          }
        }
      }
      
      # # Securities ------------------------------------------------------------
      
      
      if ("step_5" %in% names(decl_raw[[i]]$unified_source) && length(decl_raw[[i]]$unified_source$step_5) > 0) {
        
        for (j in 1:length(decl_raw[[i]]$unified_source$step_5)) {
          
          if (decl_raw[[i]]$unified_source$step_5[[j]] != "У суб'єкта декларування відсутні об'єкти для декларування в цьому розділі.")
          {
            rights <- ""
            
            if ("rights" %in% names(decl_raw[[i]]$unified_source$step_5[[j]]) && 
                length(decl_raw[[i]]$unified_source$step_5[[j]]$rights) > 0) {
              
              for (k in 1:length(decl_raw[[i]]$unified_source$step_5[[j]]$rights)) {
                rights <- paste0(rights, decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$seller, ": ",
                                 decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$citizen, ", ",
                                 ifelse(decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$citizen == "Громадянин України",
                                        paste0(decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$ua_lastname, " ",
                                               decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$ua_firstname, " ",
                                               decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$ua_middlename, ";"),
                                        ifelse(decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$citizen == "Іноземний громадянин", 
                                               paste0(decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$eng_lastname, " ",
                                                      decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$eng_firstname, " ",
                                                      decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$eng_middlename, ";"),
                                               ifelse(decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована в Україні", 
                                                      paste0(decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$ua_company_name, " ",
                                                             decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$ua_company_code),
                                                      ifelse(decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована за кордоном", 
                                                             paste0(decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$eng_company_name, " ",
                                                                    decl_raw[[i]]$unified_source$step_5[[j]]$rights[[k]]$eng_company_code),
                                                             "?")))))
              }
            }
            
            securities <- rbindlist(list(securities,
                                         list(decl_raw[[i]]$infocard$url,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$person,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$typeProperty,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$subTypeProperty,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$otherObjectType,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$owningDate,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$amount,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$cost,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$costDate,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$costLast,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$emitent,
                                              decl_raw[[i]]$unified_source$step_5[[j]]$emitent_type,
                                              paste0(decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ua_lastname, " ",
                                                     decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ua_firstname, " ",
                                                     decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ua_middlename),
                                              ifelse(is.null(decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ukr_fullname), "",
                                                     decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ukr_fullname),
                                              ifelse(is.null(decl_raw[[i]]$unified_source$step_5[[j]]$emitent_eng_fullname), "",
                                                     decl_raw[[i]]$unified_source$step_5[[j]]$emitent_eng_fullname),
                                              ifelse(is.null(decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ua_company_name), "",
                                                     decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ua_company_name),
                                              ifelse(is.null(decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ukr_company_name), "",
                                                     decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ukr_company_name),
                                              ifelse(is.null(decl_raw[[i]]$unified_source$step_5[[j]]$emitent_eng_company_name), "",
                                                     decl_raw[[i]]$unified_source$step_5[[j]]$emitent_eng_company_name),
                                              ifelse(is.null(decl_raw[[i]]$unified_source$step_5[[j]]$emitent_eng_company_code),
                                                     "",
                                                     decl_raw[[i]]$unified_source$step_5[[j]]$emitent_eng_company_code),
                                              ifelse(is.null(decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ua_company_code),
                                                     "",
                                                     decl_raw[[i]]$unified_source$step_5[[j]]$emitent_ua_company_code),
                                              rights)))
          }
        } 
      }
      # # Corporate rights ------------------------------------------------------
      
      if ("step_6" %in% names(decl_raw[[i]]$unified_source) && length(decl_raw[[i]]$unified_source$step_6) > 0) {
        
        for (j in 1:length(decl_raw[[i]]$unified_source$step_6)) {
          if (decl_raw[[i]]$unified_source$step_6[[j]] != "У суб'єкта декларування відсутні об'єкти для декларування в цьому розділі.")
          {
            rights <- ""
            
            if ("rights" %in% names(decl_raw[[i]]$unified_source$step_6[[j]]) && 
                length(decl_raw[[i]]$unified_source$step_6[[j]]$rights) > 0) {
              
              for (k in 1:length(decl_raw[[i]]$unified_source$step_6[[j]]$rights)) {
                rights <- paste0(rights, decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$seller, ": ",
                                 decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$citizen, ", ",
                                 ifelse(decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$citizen == "Громадянин України",
                                        paste0(decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$ua_lastname, " ",
                                               decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$ua_firstname, " ",
                                               decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$ua_middlename, ";"),
                                        ifelse(decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$citizen == "Іноземний громадянин", 
                                               decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$eng_fullname,
                                               ifelse(decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована в Україні", 
                                                      paste0(decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$ua_company_name, " ",
                                                             decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$ua_company_code),
                                                      ifelse(decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована за кордоном", 
                                                             paste0(decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$eng_company_name, " ",
                                                                    decl_raw[[i]]$unified_source$step_6[[j]]$rights[[k]]$eng_company_code),
                                                             "?")))))
              }
            }
            
            corp_rights <- rbindlist(list(corp_rights,
                                          list(decl_raw[[i]]$infocard$url,
                                               decl_raw[[i]]$unified_source$step_6[[j]]$person,
                                               decl_raw[[i]]$unified_source$step_6[[j]]$name,
                                               decl_raw[[i]]$unified_source$step_6[[j]]$country,
                                               ifelse(is.null(decl_raw[[i]]$unified_source$step_6[[j]]$corporate_rights_company_code),
                                                      "", decl_raw[[i]]$unified_source$step_6[[j]]$corporate_rights_company_code),
                                               decl_raw[[i]]$unified_source$step_6[[j]]$legalForm,
                                               decl_raw[[i]]$unified_source$step_6[[j]]$cost,
                                               decl_raw[[i]]$unified_source$step_6[[j]]$cost_percent,
                                               decl_raw[[i]]$unified_source$step_6[[j]]$costDate,
                                               decl_raw[[i]]$unified_source$step_6[[j]]$owningDate,
                                               rights)))
          }
        }
      }
      
      # # Movables --------------------------------------------------------------
      
      if ("step_7" %in% names(decl_raw[[i]]$unified_source) && length(decl_raw[[i]]$unified_source$step_7) > 0) {
        
        for (j in 1:length(decl_raw[[i]]$unified_source$step_7)) {
          if (decl_raw[[i]]$unified_source$step_7[[j]] != "У суб'єкта декларування відсутні об'єкти для декларування в цьому розділі.")
          {
            rights <- ""
            
            if ("rights" %in% names(decl_raw[[i]]$unified_source$step_7[[j]]) && 
                length(decl_raw[[i]]$unified_source$step_7[[j]]$rights) > 0) {
              
              for (k in 1:length(decl_raw[[i]]$unified_source$step_7[[j]]$rights)) {
                rights <- paste0(rights, decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$seller, ": ",
                                 decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$citizen, ", ",
                                 ifelse(decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$citizen == "Громадянин України",
                                        paste0(decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$ua_lastname, " ",
                                               decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$ua_firstname, " ",
                                               decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$ua_middlename, ";"),
                                        ifelse(decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$citizen == "Іноземний громадянин", 
                                               paste0(decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$eng_lastname, " ",
                                                      decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$eng_firstname, " ",
                                                      decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$eng_middlename, ";"),
                                               ifelse(decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована в Україні", 
                                                      paste0(decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$ua_company_name, " ",
                                                             decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$ua_company_code),
                                                      ifelse(decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована за кордоном", 
                                                             paste0(decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$eng_company_name, " ",
                                                                    decl_raw[[i]]$unified_source$step_7[[j]]$rights[[k]]$eng_company_code),
                                                             "?")))))
              }
            }
            
            movables <- rbindlist(list(movables,
                                       list(decl_raw[[i]]$infocard$url,
                                            decl_raw[[i]]$unified_source$step_7[[j]]$person,
                                            decl_raw[[i]]$unified_source$step_7[[j]]$objectType,
                                            ifelse(is.null(decl_raw[[i]]$unified_source$step_7[[j]]$otherObjectType), 
                                                   "",
                                                   decl_raw[[i]]$unified_source$step_7[[j]]$otherObjectType),
                                            decl_raw[[i]]$unified_source$step_7[[j]]$dateUse,
                                            decl_raw[[i]]$unified_source$step_7[[j]]$trademark,
                                            decl_raw[[i]]$unified_source$step_7[[j]]$manufacturerName,
                                            gsub("[\r\n]", ", ", decl_raw[[i]]$unified_source$step_7[[j]]$propertyDescr),
                                            decl_raw[[i]]$unified_source$step_7[[j]]$costDateUse,
                                            decl_raw[[i]]$unified_source$step_7[[j]]$costLast,
                                            rights)))
          }
        }
      }
      
      
      # # NMA -------------------------------------------------------------------
      
      if ("step_8" %in% names(decl_raw[[i]]$unified_source) && length(decl_raw[[i]]$unified_source$step_8) > 0) {
        
        for (j in 1:length(decl_raw[[i]]$unified_source$step_8)) {
          if (decl_raw[[i]]$unified_source$step_8[[j]] != "У суб'єкта декларування відсутні об'єкти для декларування в цьому розділі.")
          {
            
            
            rights <- ""
            
            if ("rights" %in% names(decl_raw[[i]]$unified_source$step_8[[j]]) && 
                length(decl_raw[[i]]$unified_source$step_8[[j]]$rights) > 0) {
              
              for (k in 1:length(decl_raw[[i]]$unified_source$step_8[[j]]$rights)) {
                rights <- paste0(rights, decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$seller, ": ",
                                 decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$citizen, ", ",
                                 ifelse(decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$citizen == "Громадянин України",
                                        paste0(decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$ua_lastname, " ",
                                               decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$ua_firstname, " ",
                                               decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$ua_middlename, ";"),
                                        ifelse(decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$citizen == "Іноземний громадянин", 
                                               paste0(decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$eng_lastname, " ",
                                                      decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$eng_firstname, " ",
                                                      decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$eng_middlename, ";"),
                                               ifelse(decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована в Україні", 
                                                      paste0(decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$ua_company_name, " ",
                                                             decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$ua_company_code),
                                                      ifelse(decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$citizen == "Юридична особа, зареєстрована за кордоном", 
                                                             paste0(decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$eng_company_name, " ",
                                                                    decl_raw[[i]]$unified_source$step_8[[j]]$rights[[k]]$eng_company_code),
                                                             "?")))))
              }
            }
            
            nma <- rbindlist(list(nma,
                                  list(decl_raw[[i]]$infocard$url,
                                       decl_raw[[i]]$unified_source$step_8[[j]]$person,
                                       decl_raw[[i]]$unified_source$step_8[[j]]$objectType,
                                       decl_raw[[i]]$unified_source$step_8[[j]]$otherObjectType,
                                       decl_raw[[i]]$unified_source$step_8[[j]]$owningDate,
                                       gsub("[\r\n]", ", ", decl_raw[[i]]$unified_source$step_8[[j]]$descriptionObject),
                                       decl_raw[[i]]$unified_source$step_8[[j]]$costLast,
                                       decl_raw[[i]]$unified_source$step_8[[j]]$costDateOrigin,
                                       rights)))
            
          }
        }
      }
      
      
      print(i)
      
    }
  }
}

write.csv(general_info, file = "general_info_18.csv")
write.csv(income, file = "income_18.csv")
write.csv(estate, file = "estate_18.csv")
write.csv(transport, file = "transport_18.csv")
write.csv(securities, file = "securities_18.csv")
write.csv(corp_rights, file = "corp_rights_18.csv")
write.csv(movables, file = "movables_18.csv")
write.csv(nma, file = "nma_18.csv")
