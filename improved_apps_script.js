function setupWorkoutSheet() {
    var ss = SpreadsheetApp.getActiveSpreadsheet();

    // --- 1. SETUP EXERCISE DATABASE (For Dropdowns) ---
    var dbSheet = ss.getSheetByName("ExerciseDB");
    if (!dbSheet) {
        dbSheet = ss.insertSheet("ExerciseDB");
        dbSheet.hideSheet();
    }
    dbSheet.clear();
    var exerciseList = [
        "Barbell Hip Thrust", "Smith Machine Hip Thrust", "KAS Glute Bridge", "B-Stance Hip Thrust", "Dumbbell Hip Thrust",
        "Romanian Deadlift", "Dumbbell RDL", "Single Leg RDL", "Cable Pull Through", "Seated Leg Curl", "Lying Leg Curl",
        "Swiss Ball Hamstring Curl", "Smith Machine Squat", "Goblet Squat (Heels Elevated)", "Leg Press", "Bulgarian Split Squat",
        "Reverse Deficit Lunges", "Step Ups", "Walking Lunges", "Curtsy Lunges", "Leg Extensions", "Sissy Squats",
        "Lat Pulldown (Wide Grip)", "Assisted Pull Up", "Neutral Grip Lat Pulldown", "Straight Arm Pulldown",
        "Seated Cable Row", "Chest Supported Row", "Single Arm Dumbbell Row", "Overhead Press", "Seated Dumbbell Press",
        "Dumbbell Lateral Raises", "Cable Lateral Raises", "Lu Raises", "Face Pulls", "Reverse Pec Deck",
        "Pushups", "Incline Dumbbell Press", "Tricep Rope Pushdowns", "Skullcrushers", "Overhead Cable Extension",
        "Dips (Assisted)", "Dumbbell Curls", "Hammer Curls", "Bayesian Curls", "Seated Abductor Machine",
        "Standing Cable Abduction", "Standing Calf Raise", "Leg Press Calf Raise", "Plank", "Deadbugs", "Russian Twists", "Cable Woodchoppers"
    ];
    dbSheet.getRange(1, 1, exerciseList.length, 1).setValues(exerciseList.map(function (e) { return [e]; }));

    // --- 2. CREATE "START HERE" INSTRUCTIONS TAB ---
    var infoSheet = ss.getSheetByName("Start Here");
    if (!infoSheet) {
        infoSheet = ss.insertSheet("Start Here", 0);
    }
    infoSheet.clear();

    var instructions = [
        ["✨ WELCOME TO YOUR TRAINING DASHBOARD ✨"],
        [""],
        ["HOW TO USE THIS SHEET"],
        ["1. Go to the 'WorkoutLog' tab."],
        ["2. Find today's workout."],
        ["3. Log your 'ACTUAL Weight' and 'ACTUAL Reps'."],
        ["4. Rate the RPE (1-10) - How hard was it?"],
        ["5. Check the box when done! ✅"],
        [""],
        ["TRACKING PROGRESS"],
        ["Check the 'Live Dashboard' tab to see your strength gains!"]
    ];

    var range = infoSheet.getRange(1, 1, instructions.length, 1);
    range.setValues(instructions);
    infoSheet.getRange("A1").setFontSize(18).setFontColor("#d81b60").setFontWeight("bold");
    infoSheet.setColumnWidth(1, 500);

    // --- 3. FORMAT "WORKOUT LOG" TAB ---
    var logSheet = ss.getSheetByName("WorkoutLog");
    if (!logSheet) {
        logSheet = ss.insertSheet("WorkoutLog");
    }
    // Force update headers to match new layout
    logSheet.getRange("A1:M1").setValues([["Week", "Day", "Exercise", "Sets", "Reps", "Rest", "Target Weight", "ACTUAL Weight", "ACTUAL Reps", "RPE", "Coach Cues", "My Notes", "Done"]]);
    logSheet.setFrozenRows(1);

    // Clear old validation from Column L (was "Done?", now "My Notes")
    logSheet.getRange("L2:L1000").clearDataValidations();
    // Clear any accidental validation from Sets/Reps (Columns D & E)
    logSheet.getRange("D2:E1000").clearDataValidations();

    // 3a. Dropdown for Exercise (Column C)
    var exerciseRange = dbSheet.getRange(1, 1, exerciseList.length, 1);
    var rule = SpreadsheetApp.newDataValidation().requireValueInRange(exerciseRange).setAllowInvalid(true).build();
    logSheet.getRange("C2:C1000").setDataValidation(rule);

    // 3b. Dropdown for RPE (Column J) - 1 to 10
    var rpeList = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"];
    var rpeRule = SpreadsheetApp.newDataValidation().requireValueInList(rpeList).setAllowInvalid(true).build();
    logSheet.getRange("J2:J1000").setDataValidation(rpeRule);

    // 3c. Checkboxes for "Done" (Column M)
    var checkboxRule = SpreadsheetApp.newDataValidation().requireCheckbox().build();
    logSheet.getRange("M2:M1000").setDataValidation(checkboxRule);

    // 3d. Conditional Formatting: Strike-through and Green when Done
    var doneRule = SpreadsheetApp.newConditionalFormatRule()
        .whenFormulaSatisfied('=$M2=TRUE')
        .setBackground("#d9ead3")
        .setFontColor("#006400")
        .setStrikethrough(true)
        .setRanges([logSheet.getRange("A2:M1000")])
        .build();
    logSheet.setConditionalFormatRules([doneRule]);

    // 3e. Alternating Colors (Banding)
    var range = logSheet.getRange("A1:M1000");
    var bandings = range.getBandings();
    if (bandings.length > 0) {
        for (var i = 0; i < bandings.length; i++) {
            bandings[i].remove();
        }
    }
    range.applyRowBanding(SpreadsheetApp.BandingTheme.LIGHT_GREY);

    // --- 4. CREATE "LIVE DASHBOARD" TAB ---
    var dashSheet = ss.getSheetByName("Live Dashboard");
    if (!dashSheet) {
        dashSheet = ss.insertSheet("Live Dashboard", 1);
    }
    dashSheet.clear();
    dashSheet.getRange("A1").setValue("🔥 LIVE STRENGTH STATS").setFontSize(16).setFontWeight("bold");
    dashSheet.getRange("A3:C3").setValues([["Key Lift", "Current Max (Calculated)", "Last Date Logged"]]).setFontWeight("bold").setBackground("#f3f3f3");
    var keyLifts = ["Barbell Hip Thrust", "Smith Machine Squat", "Romanian Deadlift", "Lat Pulldown (Wide Grip)", "Overhead Press"];
    for (var i = 0; i < keyLifts.length; i++) {
        var row = i + 4;
        var lift = keyLifts[i];
        dashSheet.getRange("A" + row).setValue(lift);
        // Updated formula to match new column C (Exercise) and G (Actual Weight is now H? No, Target is G, Actual is H)
        // Col C = Exercise. Col H = Actual Weight.
        dashSheet.getRange("B" + row).setFormula(`=MAXIFS(WorkoutLog!H:H, WorkoutLog!C:C, "${lift}")`);
        dashSheet.getRange("C" + row).setValue("Auto-Updated");
    }

    SpreadsheetApp.getUi().alert("System Upgraded! Checkboxes & RPE added.");
}

function onOpen() {
    var ui = SpreadsheetApp.getUi();
    ui.createMenu('💪 Workout Plan')
        .addItem('Run Setup / Reset Styles', 'setupWorkoutSheet')
        .addToUi();
}
