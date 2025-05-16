import Foundation

// Database structure to store passwords and last updated timestamps
struct Database: Codable {
    var db1: [String: String]  // Stores [keyword: password]
    var db2: [String: String]  // Stores [keyword: lastModified]
}

// Global file path for the database file
var filePath: String = ""

// Reset the database file by writing empty dictionaries
func resetDbFile() {
    let emptyDb = Database(db1: [:], db2: [:])
    if let data = try? JSONEncoder().encode(emptyDb) {
        try? data.write(to: URL(fileURLWithPath: filePath))
    }
}

// Load the database from disk
func loadDatabase() -> Database {
    let url = URL(fileURLWithPath: filePath)
    if let data = try? Data(contentsOf: url),
       let db = try? JSONDecoder().decode(Database.self, from: data) {
        return db
    }
    return Database(db1: [:], db2: [:])
}

// Save the database to disk
func saveDatabase(_ db: Database) {
    if let data = try? JSONEncoder().encode(db) {
        try? data.write(to: URL(fileURLWithPath: filePath))
    }
}

// Generate a random character from one of the character groups
func getRandomCharacter(group: Int = 4) -> String {
    let characters: [[String]] = [
        Array("ABCDEFGHIJKLMNOPQRSTUVWXYZ").map { String($0) },
        Array("abcdefghijklmnopqrstuvwxyz").map { String($0) },
        Array("0123456789").map { String($0) },
        ["~", "!", "@", "#", "$", "%", "&", "*", "(", ")", "-", "_", "=", "+", "[", "]", "|", ";", ":", "'", ",", "<", ".", ">", "/", "?"]
    ]
    var randomSet: [String]
    if group == 4 {
        randomSet = characters[Int.random(in: 0..<4)]
    } else {
        randomSet = characters[group]
    }
    return randomSet.randomElement()!
}

// Get the current date and time in IST (GMT+5:30) and format it
func getDateTime() -> String {
    let now = Date()
    // IST is GMT+5:30 (19800 seconds offset)
    let istTimeZone = TimeZone(secondsFromGMT: 19800)!
    var calendar = Calendar.current
    calendar.timeZone = istTimeZone
    let components = calendar.dateComponents([.day, .month, .year, .hour, .minute, .second], from: now)
    let monthNames = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    let day = components.day ?? 0
    let month = components.month ?? 0
    let year = components.year ?? 0
    var hour = components.hour ?? 0
    let minute = components.minute ?? 0
    let second = components.second ?? 0
    let period = hour >= 12 ? "PM" : "AM"
    if hour > 12 {
        hour -= 12
    }
    let timeString = String(format: "%d:%02d:%02d %@", hour, minute, second, period)
    return "on \(day) \(monthNames[month]) \(year) at \(timeString)"
}

// Print password information in a table format
func printPasswordsAsTable(_ data: [[String]]) {
    let headerLabels = ["Serial No.", "Keyword", "Password", "Last Updated"]
    var passwordInfo = data
    let noOfPasswords = data.count
    var widthOfColumns = Array(repeating: 0, count: headerLabels.count)
    
    // Calculate widths from data (skipping Serial No. for now)
    for row in 0..<noOfPasswords {
        for column in 0..<(headerLabels.count - 1) {
            widthOfColumns[column + 1] = max(widthOfColumns[column + 1], passwordInfo[row][column].count)
        }
    }
    for column in 0..<headerLabels.count {
        widthOfColumns[column] = max(widthOfColumns[column], headerLabels[column].count)
    }
    let serialWidth = "\(noOfPasswords).".count
    widthOfColumns[0] = max(widthOfColumns[0], serialWidth)
    
    // Insert serial numbers
    for i in 0..<noOfPasswords {
        let serial = "\(i + 1)."
        let padded = String(repeating: " ", count: widthOfColumns[0] - serial.count) + serial
        passwordInfo[i].insert(padded, at: 0)
    }
    
    var border = ""
    for width in widthOfColumns {
        border += "+" + String(repeating: "-", count: width + 2)
    }
    border += "+"
    print(border)
    
    // Print headers
    var headerRow = ""
    for (index, label) in headerLabels.enumerated() {
        let padding = String(repeating: " ", count: widthOfColumns[index] - label.count)
        headerRow += "| " + label + padding + " "
    }
    headerRow += "|"
    print(headerRow)
    print(border)
    
    // Print each row of password information
    for row in passwordInfo {
        var rowString = ""
        for (col, cell) in row.enumerated() {
            let padding = String(repeating: " ", count: widthOfColumns[col] - cell.count)
            rowString += "| " + cell + padding + " "
        }
        rowString += "|"
        print(rowString)
    }
    print(border)
}

// Setup the database file path based on the operating system
let fileManager = FileManager.default
let home = NSHomeDirectory()

#if os(macOS)
    var dbFolder = "\(home)/Library/Application Support/pwdmanagerpy"
    if !fileManager.fileExists(atPath: dbFolder) {
        try? fileManager.createDirectory(atPath: dbFolder, withIntermediateDirectories: true, attributes: nil)
    }
    filePath = "\(dbFolder)/passwords.db"
#elseif os(Linux)
    var dbFolder = "\(home)/.pwdmanagerpy"
    if !fileManager.fileExists(atPath: dbFolder) {
        try? fileManager.createDirectory(atPath: dbFolder, withIntermediateDirectories: true, attributes: nil)
    }
    filePath = "\(dbFolder)/passwords.db"
#elseif os(Windows)
    var dbFolder = "\(home)\\AppData\\Roaming\\pwdmanagerpy"
    if !fileManager.fileExists(atPath: dbFolder) {
        try? fileManager.createDirectory(atPath: dbFolder, withIntermediateDirectories: true, attributes: nil)
    }
    filePath = "\(dbFolder)\\passwords.db"
#else
    filePath = "passwords.db"
    print("\n\n\nIf you wish to move this program to another location, you must carry the 'passwords.db' file along with it, otherwise all your saved passwords will get lost.")
#endif

// Initialize database if file doesn't exist or is corrupted
if !fileManager.fileExists(atPath: filePath) {
    resetDbFile()
} else {
    _ = loadDatabase()
}

// Main program loop
while true {
    var db = loadDatabase()
    
    // Display menu
    print("\n\nWhat do you want to do?\n")
    print("1. Generate Password")
    print("2. Save Password")
    print("3. Update Password")
    print("4. View Password")
    print("5. Delete Password")
    print("6. Quit\n")
    print("Enter your choice: ", terminator: "")
    guard let userChoice = readLine(), let choiceInt = Int(userChoice), (1...6).contains(choiceInt) else { continue }
    
    if choiceInt == 1 {
        // Generate Password
        print("\nEnter the length of the password that you want to create (a whole number between 8 and 32): ", terminator: "")
        guard let lengthInput = readLine(), let length = Int(lengthInput), (8...32).contains(length) else {
            print("Invalid length.")
            continue
        }
        
        print("\nGenerating Password...", terminator: "")
        sleep(1)
        var password = ""
        password += getRandomCharacter(group: 0)
        password += getRandomCharacter(group: 1)
        password += getRandomCharacter(group: 2)
        password += getRandomCharacter(group: 3)
        for _ in 0..<(length - 4) {
            password += getRandomCharacter()
        }
        
        print("\n\nThe generated password is: \(password)")
        sleep(1)
        
        print("\nDo you want to save this password? [Yes / No] ", terminator: "")
        if let saveChoice = readLine(), saveChoice.lowercased() == "yes" || saveChoice.lowercased() == "y" {
            print("Enter a unique keyword with which you can identify your password later: ", terminator: "")
            var passwordKey = readLine() ?? ""
            while passwordKey.lowercased() == "all" || db.db1[passwordKey] != nil {
                if passwordKey.lowercased() == "all" {
                    print("The keyword can't be 'all'; please enter another keyword: ", terminator: "")
                } else {
                    print("A password has already been saved with this keyword; please enter another keyword: ", terminator: "")
                }
                passwordKey = readLine() ?? ""
            }
            db.db1[passwordKey] = password
            db.db2[passwordKey] = getDateTime()
            saveDatabase(db)
            print("\nPassword saved successfully.")
        }
    } else if choiceInt == 2 {
        // Save Password manually
        print("\nEnter the password that you want to save: ", terminator: "")
        guard let password = readLine() else { continue }
        print("Enter a unique keyword with which you can identify your password later: ", terminator: "")
        var passwordKey = readLine() ?? ""
        while passwordKey.lowercased() == "all" || db.db1[passwordKey] != nil {
            if passwordKey.lowercased() == "all" {
                print("The keyword can't be 'all'; please enter another keyword: ", terminator: "")
            } else {
                print("A password has already been saved with this keyword; please enter another keyword: ", terminator: "")
            }
            passwordKey = readLine() ?? ""
        }
        db.db1[passwordKey] = password
        db.db2[passwordKey] = getDateTime()
        saveDatabase(db)
        print("\nPassword saved successfully.")
    } else if choiceInt == 3 {
        // Update Password
        if db.db1.isEmpty {
            print("\nNo password has been saved.")
        } else {
            var passwordInfo: [[String]] = []
            for key in db.db1.keys {
                let pass = db.db1[key] ?? ""
                let modified = db.db2[key] ?? ""
                passwordInfo.append([key, pass, modified])
            }
            print("")
            printPasswordsAsTable(passwordInfo)
            print("\nEnter the keyword for the password that you want to update: ", terminator: "")
            if let key = readLine(), db.db1.keys.contains(key) {
                print("Enter a new password for the keyword ‘\(key)’: ", terminator: "")
                if let newPassword = readLine() {
                    db.db1[key] = newPassword
                    db.db2[key] = getDateTime()
                    saveDatabase(db)
                    print("\nPassword updated successfully.")
                }
            } else {
                print("\nNo password has been saved with this keyword.")
            }
        }
    } else if choiceInt == 4 {
        // View Password
        if db.db1.isEmpty {
            print("\nNo password has been saved.")
        } else {
            print("\nEnter the keyword for the password that you want to view (enter ‘all’ if you want to view all the passwords): ", terminator: "")
            if let key = readLine() {
                if key.lowercased() == "all" {
                    var passwordInfo: [[String]] = []
                    for k in db.db1.keys {
                        let pass = db.db1[k] ?? ""
                        let modified = db.db2[k] ?? ""
                        passwordInfo.append([k, pass, modified])
                    }
                    print("")
                    printPasswordsAsTable(passwordInfo)
                } else if db.db1[key] != nil {
                    let pass = db.db1[key] ?? ""
                    let modified = db.db2[key] ?? ""
                    print("")
                    printPasswordsAsTable([[key, pass, modified]])
                } else {
                    print("\nNo password has been saved with this keyword.")
                }
            }
        }
    } else if choiceInt == 5 {
        // Delete Password
        if db.db1.isEmpty {
            print("\nNo password has been saved.")
        } else {
            var passwordInfo: [[String]] = []
            for key in db.db1.keys {
                let pass = db.db1[key] ?? ""
                let modified = db.db2[key] ?? ""
                passwordInfo.append([key, pass, modified])
            }
            print("")
            printPasswordsAsTable(passwordInfo)
            print("\nEnter the keyword for the password that you want to delete (enter ‘all’ if you want to delete all the passwords): ", terminator: "")
            if let key = readLine() {
                if key.lowercased() == "all" {
                    resetDbFile()
                    db = loadDatabase()
                    print("\nPasswords deleted successfully.")
                } else if db.db1[key] != nil {
                    db.db1.removeValue(forKey: key)
                    db.db2.removeValue(forKey: key)
                    saveDatabase(db)
                    print("\nPassword deleted successfully.")
                } else {
                    print("\nNo password has been saved with this keyword.")
                }
            }
        }
    } else {
        print("\n\n\n")
        break
    }
    sleep(1)
}