/**
 * ==============================================================================
 * DON BOSCO YOUTH CENTRE (DBYC) - BASIN BRIDGE, CHENNAI - 600 012
 * OFFICIAL GOOGLE APPS SCRIPT BACKEND (Code.gs)
 * ==============================================================================
 * - Structured Data: Saved ONLY in Google Sheets (Spreadsheet tabs)
 * - Media Files: Photos and Videos saved in Google Drive (DBYC_Media_Uploads)
 * - Zero Captcha: Direct, high-speed, frictionless member registration
 * - 10-Second Auto Refresh: Real-time sync across all mobiles and PCs
 * ==============================================================================
 */

// Configuration constants
var SPREADSHEET_NAME = "DBYC_BasinBridge_Database";
var DRIVE_FOLDER_NAME = "DBYC_Media_Uploads";

/**
 * Handle incoming GET requests (Sync data retrieval, member listing, ping, and Web App UI)
 */
function doGet(e) {
  try {
    var params = e ? e.parameter : {};
    var action = params.action;
    
    // 1. Direct Web App UI Service: When opened in browser without API action
    if (action === "APP" || action === "UI" || (!action && !params.get && !params.id)) {
      try {
        return HtmlService.createHtmlOutputFromFile('index')
          .setTitle("DBYC - Don Bosco Youth Centre | Basin Bridge, Chennai - 600 012")
          .addMetaTag('viewport', 'width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no')
          .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
      } catch (htmlErr) {
        // Fallback to JSON payload if index.html is not added to the GAS project
      }
    }
    
    var activeAction = action || "SYNC_GET";
    var ss = getOrCreateSpreadsheet();
    
    if (activeAction === "PING") {
      return jsonResponse({
        status: "success",
        message: "DBYC Google Sheets & Drive Backend is Live",
        spreadsheetId: ss.getId(),
        spreadsheetUrl: ss.getUrl(),
        timestamp: new Date().toISOString()
      });
    }
    
    if (activeAction === "GET_MEMBERS") {
      var members = readSheetObjects(ss, "Members");
      return jsonResponse({ status: "success", count: members.length, data: members });
    }
    
    // Default: SYNC_GET - Full application synchronization payload
    var payload = {
      updatedAt: new Date().toISOString(),
      members: readSheetObjects(ss, "Members"),
      attendance: readSheetObjects(ss, "Attendance"),
      news: readSheetObjects(ss, "News"),
      events: readSheetObjects(ss, "Events"),
      minutes: readSheetObjects(ss, "Minutes"),
      qualifications: readSheetObjects(ss, "Qualifications"),
      matches: readSheetObjects(ss, "Matches"),
      settings: readKeyValueSheet(ss, "Settings")
    };
    
    return jsonResponse({ status: "success", data: payload });
  } catch (err) {
    return jsonResponse({ status: "error", message: err.toString(), stack: err.stack });
  }
}

/**
 * Handle incoming POST requests (Register member, upload media, update, sync save)
 */
function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return jsonResponse({ status: "error", message: "No post data received" });
    }
    
    var body = JSON.parse(e.postData.contents);
    var action = body.action || "SYNC_SAVE";
    var ss = getOrCreateSpreadsheet();
    
    // 1. Upload Photo or Video to Google Drive
    if (action === "UPLOAD_MEDIA") {
      var mediaResult = uploadMediaToDrive(body);
      return jsonResponse({
        status: "success",
        fileId: mediaResult.fileId,
        url: mediaResult.url,
        viewUrl: mediaResult.viewUrl,
        downloadUrl: mediaResult.downloadUrl,
        name: mediaResult.name
      });
    }
    
    // 2. Direct Member Registration (Zero Captcha - Direct to Google Sheet)
    if (action === "REGISTER_MEMBER") {
      var member = body.member || body.data;
      var memberRow = upsertMemberInSheet(ss, member);
      
      // Also add entry to Qualifications tab for approval tracking
      upsertQualificationInSheet(ss, {
        id: "QUAL-" + (member.id || ("MEM-" + new Date().getTime())),
        type: "MEMBER_REGISTRATION",
        submitterId: member.id || "",
        submitterName: member.name || "New Registered Member",
        details: (member.role || "Member") + " | " + (member.mobile || "") + " | Acts: " + (member.activities || ""),
        submissionDate: new Date().toISOString(),
        status: member.approvalStatus || "PENDING",
        approvedBy: member.approvedBy || "",
        approvedDate: member.approvedDate || ""
      });
      
      return jsonResponse({
        status: "success",
        message: "Member registered successfully in Google Sheet",
        member: memberRow
      });
    }
    
    // 3. Mark Attendance
    if (action === "SAVE_ATTENDANCE") {
      var att = body.attendance || body.data;
      appendRowToSheet(ss, "Attendance", [
        new Date().toISOString(),
        att.date || new Date().toISOString().split("T")[0],
        att.memberId || "",
        att.name || "",
        att.role || "",
        att.activity || "",
        att.time || new Date().toLocaleTimeString(),
        att.status || "PRESENT",
        att.markedBy || "Leader"
      ]);
      return jsonResponse({ status: "success", message: "Attendance recorded in Google Sheet" });
    }
    
    // 4. Submit News or Announcement
    if (action === "SAVE_NEWS") {
      var newsItem = body.news || body.data;
      upsertRowInSheet(ss, "News", "id", newsItem);
      return jsonResponse({ status: "success", message: "News saved in Google Sheet" });
    }
    
    // 5. Submit Event or Minutes
    if (action === "SAVE_EVENT") {
      upsertRowInSheet(ss, "Events", "id", body.event || body.data);
      return jsonResponse({ status: "success", message: "Event saved in Google Sheet" });
    }
    if (action === "SAVE_MINUTES") {
      upsertRowInSheet(ss, "Minutes", "id", body.minute || body.data);
      return jsonResponse({ status: "success", message: "Minutes saved in Google Sheet" });
    }
    
    // 6. Approval / Rejection Update
    if (action === "UPDATE_APPROVAL") {
      var qual = body.qualification || body.data;
      upsertRowInSheet(ss, "Qualifications", "id", qual);
      
      // If approving a member, also update their status in the Members sheet
      if (qual.type === "MEMBER_REGISTRATION" && qual.submitterId) {
        updateMemberField(ss, qual.submitterId, "approvalStatus", qual.status);
      }
      return jsonResponse({ status: "success", message: "Approval status updated in Google Sheet" });
    }
    
    // 7. Full Batch Sync Save (SYNC_SAVE)
    if (action === "SYNC_SAVE") {
      var data = body.data || body;
      
      // Batch sync members
      if (data.members && Array.isArray(data.members)) {
        syncArrayToSheet(ss, "Members", data.members, "id");
      }
      // Batch sync news
      if (data.news && Array.isArray(data.news)) {
        syncArrayToSheet(ss, "News", data.news, "id");
      }
      // Batch sync attendance
      if (data.attendance && Array.isArray(data.attendance)) {
        syncArrayToSheet(ss, "Attendance", data.attendance, "id");
      }
      // Batch sync events
      if (data.events && Array.isArray(data.events)) {
        syncArrayToSheet(ss, "Events", data.events, "id");
      }
      // Batch sync minutes
      if (data.minutes && Array.isArray(data.minutes)) {
        syncArrayToSheet(ss, "Minutes", data.minutes, "id");
      }
      // Batch sync qualifications
      if (data.qualifications && Array.isArray(data.qualifications)) {
        syncArrayToSheet(ss, "Qualifications", data.qualifications, "id");
      }
      // Batch sync matches
      if (data.matches && Array.isArray(data.matches)) {
        syncArrayToSheet(ss, "Matches", data.matches, "id");
      }
      
      // Update Settings metadata
      writeKeyValueSheet(ss, "Settings", {
        lastSyncedAt: new Date().toISOString(),
        lastSyncedBy: data.updatedBy || "DBYC Device",
        masterEditActive: data.masterEditActive ? "true" : "false"
      });
      
      return jsonResponse({
        status: "success",
        message: "All DBYC data synchronized successfully into Google Sheets",
        timestamp: new Date().toISOString()
      });
    }
    
    return jsonResponse({ status: "warning", message: "Unknown action: " + action });
  } catch (err) {
    return jsonResponse({ status: "error", message: err.toString(), stack: err.stack });
  }
}

/**
 * Upload a Photo or Video to dedicated Google Drive folder
 */
function uploadMediaToDrive(body) {
  var folder = getOrCreateDriveFolder();
  var fileName = body.fileName || ("dbyc_upload_" + new Date().getTime());
  var mimeType = body.mimeType || "image/jpeg";
  var base64Data = body.base64Data || body.data;
  
  if (base64Data && base64Data.indexOf(",") > -1) {
    base64Data = base64Data.split(",")[1];
  }
  
  var decodedBytes = Utilities.base64Decode(base64Data);
  var blob = Utilities.newBlob(decodedBytes, mimeType, fileName);
  var file = folder.createFile(blob);
  
  // Make file publicly viewable via direct link
  try {
    file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
  } catch(e) {}
  
  var fileId = file.getId();
  // Generate high-speed CDN direct image/video preview URL
  var directViewUrl = "https://lh3.googleusercontent.com/d/" + fileId;
  var downloadUrl = file.getDownloadUrl();
  
  return {
    fileId: fileId,
    name: file.getName(),
    url: directViewUrl,
    viewUrl: file.getUrl(),
    downloadUrl: downloadUrl
  };
}

/**
 * Locate or Create Google Spreadsheet
 */
function getOrCreateSpreadsheet() {
  var files = DriveApp.getFilesByName(SPREADSHEET_NAME);
  var ss;
  if (files.hasNext()) {
    ss = SpreadsheetApp.open(files.next());
  } else {
    ss = SpreadsheetApp.create(SPREADSHEET_NAME);
    initSpreadsheetHeaders(ss);
  }
  return ss;
}

/**
 * Locate or Create Google Drive Media Folder
 */
function getOrCreateDriveFolder() {
  var folders = DriveApp.getFoldersByName(DRIVE_FOLDER_NAME);
  if (folders.hasNext()) {
    return folders.next();
  }
  var folder = DriveApp.createFolder(DRIVE_FOLDER_NAME);
  try {
    folder.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
  } catch(e) {}
  return folder;
}

/**
 * Initialize all Sheet Headers if they do not exist
 */
function initSpreadsheetHeaders(ss) {
  var schema = {
    "Members": [
      "id", "name", "tamilName", "mobile", "email", "role", "roles", "category",
      "dob", "bloodGroup", "activities", "abilities", "achievements", "address",
      "emergencyPhone", "photo", "passUrl", "password", "pin", "status",
      "approvalStatus", "tenure", "group", "createdAt", "updatedAt"
    ],
    "Attendance": [
      "timestamp", "date", "memberId", "name", "role", "activity", "time", "status", "markedBy"
    ],
    "News": [
      "id", "title", "titleTa", "content", "priority", "category", "date",
      "status", "approvalStatus", "author", "mediaUrl", "createdAt"
    ],
    "Events": [
      "id", "title", "titleTa", "date", "time", "venue", "description", "category", "approvalStatus"
    ],
    "Minutes": [
      "id", "title", "date", "content", "recordedBy", "attendees", "approvalStatus"
    ],
    "Qualifications": [
      "id", "type", "submitterId", "submitterName", "details", "submissionDate", "status", "approvedBy", "approvedDate"
    ],
    "Matches": [
      "id", "sport", "teamA", "teamB", "scoreA", "scoreB", "status", "updatedAt"
    ],
    "Settings": [
      "key", "value", "updatedAt"
    ]
  };
  
  for (var sheetName in schema) {
    var sheet = ss.getSheetByName(sheetName);
    if (!sheet) {
      sheet = ss.insertSheet(sheetName);
      sheet.appendRow(schema[sheetName]);
      formatHeaderRow(sheet);
    }
  }
  
  // Remove default "Sheet1" if present
  var defaultSheet = ss.getSheetByName("Sheet1");
  if (defaultSheet && ss.getSheets().length > 1) {
    try { ss.deleteSheet(defaultSheet); } catch(e) {}
  }
}

function formatHeaderRow(sheet) {
  var range = sheet.getRange(1, 1, 1, sheet.getLastColumn());
  range.setBackground("#002b66");
  range.setFontColor("#ffffff");
  range.setFontWeight("bold");
  sheet.setFrozenRows(1);
}

/**
 * Read all rows from a sheet as an array of JSON objects
 */
function readSheetObjects(ss, sheetName) {
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) return [];
  
  var values = sheet.getDataRange().getValues();
  if (values.length <= 1) return [];
  
  var headers = values[0];
  var rows = [];
  
  for (var i = 1; i < values.length; i++) {
    var row = values[i];
    var obj = {};
    var hasData = false;
    
    for (var j = 0; j < headers.length; j++) {
      var header = headers[j];
      var cell = row[j];
      if (cell !== "" && cell !== null && cell !== undefined) {
        hasData = true;
      }
      obj[header] = cell;
    }
    
    if (hasData && obj.id !== "") {
      // Parse array fields if stored as JSON string
      if (obj.activities && typeof obj.activities === "string" && obj.activities.indexOf("[") === 0) {
        try { obj.activities = JSON.parse(obj.activities); } catch(e) {}
      }
      if (obj.roles && typeof obj.roles === "string" && obj.roles.indexOf("[") === 0) {
        try { obj.roles = JSON.parse(obj.roles); } catch(e) {}
      }
      rows.push(obj);
    }
  }
  
  return rows;
}

/**
 * Upsert Member in Sheet
 */
function upsertMemberInSheet(ss, member) {
  var sheet = ss.getSheetByName("Members");
  if (!sheet) {
    initSpreadsheetHeaders(ss);
    sheet = ss.getSheetByName("Members");
  }
  
  var values = sheet.getDataRange().getValues();
  var headers = values[0];
  var idCol = headers.indexOf("id");
  var rowIndex = -1;
  
  for (var i = 1; i < values.length; i++) {
    if (values[i][idCol] === member.id || (member.mobile && values[i][headers.indexOf("mobile")] === member.mobile)) {
      rowIndex = i + 1;
      break;
    }
  }
  
  var rowData = [];
  for (var j = 0; j < headers.length; j++) {
    var h = headers[j];
    var val = member[h];
    if (Array.isArray(val)) {
      val = JSON.stringify(val);
    } else if (val === undefined || val === null) {
      val = "";
    }
    rowData.push(val);
  }
  
  if (rowIndex > -1) {
    sheet.getRange(rowIndex, 1, 1, rowData.length).setValues([rowData]);
  } else {
    sheet.appendRow(rowData);
  }
  
  return member;
}

/**
 * Upsert Qualification in Sheet
 */
function upsertQualificationInSheet(ss, qual) {
  return upsertRowInSheet(ss, "Qualifications", "id", qual);
}

/**
 * Generic Upsert row by key in any sheet
 */
function upsertRowInSheet(ss, sheetName, keyField, obj) {
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    initSpreadsheetHeaders(ss);
    sheet = ss.getSheetByName(sheetName);
  }
  
  var values = sheet.getDataRange().getValues();
  var headers = values[0];
  var keyCol = headers.indexOf(keyField);
  var rowIndex = -1;
  
  if (keyCol > -1) {
    for (var i = 1; i < values.length; i++) {
      if (values[i][keyCol] === obj[keyField]) {
        rowIndex = i + 1;
        break;
      }
    }
  }
  
  var rowData = [];
  for (var j = 0; j < headers.length; j++) {
    var h = headers[j];
    var val = obj[h];
    if (Array.isArray(val) || (typeof val === "object" && val !== null)) {
      val = JSON.stringify(val);
    } else if (val === undefined || val === null) {
      val = "";
    }
    rowData.push(val);
  }
  
  if (rowIndex > -1) {
    sheet.getRange(rowIndex, 1, 1, rowData.length).setValues([rowData]);
  } else {
    sheet.appendRow(rowData);
  }
  return obj;
}

/**
 * Batch synchronize array of objects to sheet
 */
function syncArrayToSheet(ss, sheetName, items, keyField) {
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    initSpreadsheetHeaders(ss);
    sheet = ss.getSheetByName(sheetName);
  }
  
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var existingValues = sheet.getDataRange().getValues();
  var keyCol = headers.indexOf(keyField);
  
  var existingMap = {};
  for (var i = 1; i < existingValues.length; i++) {
    var key = existingValues[i][keyCol];
    if (key) existingMap[key] = i + 1;
  }
  
  for (var k = 0; k < items.length; k++) {
    var item = items[k];
    if (!item) continue;
    
    var rowData = [];
    for (var h = 0; h < headers.length; h++) {
      var headerName = headers[h];
      var v = item[headerName];
      if (Array.isArray(v) || (typeof v === "object" && v !== null)) {
        v = JSON.stringify(v);
      } else if (v === undefined || v === null) {
        v = "";
      }
      rowData.push(v);
    }
    
    var keyValue = item[keyField];
    if (keyValue && existingMap[keyValue]) {
      sheet.getRange(existingMap[keyValue], 1, 1, rowData.length).setValues([rowData]);
    } else {
      sheet.appendRow(rowData);
      if (keyValue) existingMap[keyValue] = sheet.getLastRow();
    }
  }
}

function updateMemberField(ss, memberId, fieldName, value) {
  var sheet = ss.getSheetByName("Members");
  if (!sheet) return;
  var values = sheet.getDataRange().getValues();
  var headers = values[0];
  var idCol = headers.indexOf("id");
  var targetCol = headers.indexOf(fieldName);
  if (idCol === -1 || targetCol === -1) return;
  
  for (var i = 1; i < values.length; i++) {
    if (values[i][idCol] === memberId) {
      sheet.getRange(i + 1, targetCol + 1).setValue(value);
      break;
    }
  }
}

function appendRowToSheet(ss, sheetName, rowData) {
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    initSpreadsheetHeaders(ss);
    sheet = ss.getSheetByName(sheetName);
  }
  sheet.appendRow(rowData);
}

function readKeyValueSheet(ss, sheetName) {
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) return {};
  var values = sheet.getDataRange().getValues();
  var res = {};
  for (var i = 1; i < values.length; i++) {
    if (values[i][0]) {
      res[values[i][0]] = values[i][1];
    }
  }
  return res;
}

function writeKeyValueSheet(ss, sheetName, obj) {
  var sheet = ss.getSheetByName(sheetName);
  if (!sheet) {
    initSpreadsheetHeaders(ss);
    sheet = ss.getSheetByName(sheetName);
  }
  for (var k in obj) {
    var values = sheet.getDataRange().getValues();
    var found = false;
    for (var i = 1; i < values.length; i++) {
      if (values[i][0] === k) {
        sheet.getRange(i + 1, 2).setValue(obj[k]);
        sheet.getRange(i + 1, 3).setValue(new Date().toISOString());
        found = true;
        break;
      }
    }
    if (!found) {
      sheet.appendRow([k, obj[k], new Date().toISOString()]);
    }
  }
}

function jsonResponse(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
