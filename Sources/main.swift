// Vedqiibyol - 2023-2024 ©

// MR references
// MR-ANN: Annotations
// 001. Use
// 002. Syntax

import Foundation
import ArgumentParser

struct mr: ParsableCommand {
  static var configuration = CommandConfiguration(
    abstract: "markright",
    usage: "mr <input> [<options>]",
    discussion: "converting Markright or Markdown files to HTML.",
    helpNames: .customShort("?"))

  @Argument(help: "Input file (path; MD/MR)")
  var input: String

  @OptionGroup(title: "Output file")
  var mrout: mroutput

  @OptionGroup(title: "Resources")
  var res: mrres

  @OptionGroup(title: "Provide informations")
  var infos: mrinfos

  @OptionGroup(title: "Webcontent and page settings")
  var web: mrweb

  // ! IMPORTANT !
  // Set back `debugcore` components for release
  @Flag(name: .long, help: .hidden) var debugcore = false
  @Option(name: .long) var mrstyle:  String = "core/markright.css"
  @Option(name: .long) var mrscript: String = "core/markright.js"

  mutating func run() throws {
    let output = mrout.output ?? input.split(separator: ".", maxSplits: 1)[0] + ".html"

    var errors: Int64 = 0
    if !FileManager.default.fileExists(atPath: input) { errors |= 1 }
    if !FileManager.default.isReadableFile(atPath: input) { errors |= 2 }

    if FileManager.default.fileExists(atPath: output) {
      if !FileManager.default.isWritableFile(atPath: output) {
        errors |= 32
      }
    } else if !FileManager.default.createFile(atPath: output, contents: nil) {
      errors |= 64
    }

    if errors != 0 {
      if (errors & 1) != 0 { print("error: could not open file '\(input)'. The files doesn't exist") }
      if (errors & 2) != 0 { print("error: could not read the file '\(input).'") }

      if (errors & 32) != 0 { print("error: output file '\(output)' exists and cannot be modified.") }
      if (errors & 64) != 0 { print("error: couldn't write file '\(output)'.") }
      return
    }

    var prod = mrprod(ctable: web.ct ? [] : nil)

    guard let ofile = FileHandle(forWritingAtPath: output) else {
      print("error: file '\(output)' was created but could not be written in.")
      return
    }

    try ofile.truncate(atOffset: 0)
    var lnum = 0

    let content = try String(contentsOfFile: input, encoding: .utf8)
    content.enumerateLines { [self] line, _ in
      lnum += 1

      // if let m = try expr.head?.firstMatch(in: line) { print(m) }
      ofile.write( parseline(line, lnum, &prod) )
    }

    if prod.emptylines != 0 { ofile.write( "</p>".data(using: .utf8) ?? Data() ) }

    try ofile.close()
  }
  // struct auto: ParsableCommand {
  //   @Option(help: "Input generation file (path; JSON)")
  //   var input: String = "schema.json"
  // }

  struct mroutput: ParsableArguments {
    @Option(name: .shortAndLong, help: "Output file (path; XML/HTML)")
    var output: String?
    @Flag(name: .long, help: "Standalone HTML with header")
    var standalone: Bool = false
    @Flag(name: .short, help: "Add all/most features")
    var full: Bool = false
  }
  struct mrres: ParsableArguments {
    @Option(name: .shortAndLong, parsing: .upToNextOption, help: "Include a stylesheet (path; CSS)")
    var styles: [String] = []
    @Option(name: [.customShort("j"), .long], parsing: .upToNextOption, help: "Include a script (path; JS)")
    var script: [String] = []
  }
  struct mrinfos: ParsableArguments {
    @Option(name: .shortAndLong, help: "Quickly include all informations, '/' to leave empty")
    var allinfos: [String] = []

    @Option(name: .long) var favicon:  String?
    @Option(name: .long) var title:    String?
    @Option(name: .long) var desc:     String?
    @Option(name: .long) var author:   String?
    @Option(name: .long) var datec:    String?
    @Option(name: .long) var datee:    String?
    @Option(name: .long) var language: String?
    @Option(name: .long) var tags:     String?
    @Option(name: .long) var version:  String?
  }
  struct mrweb: ParsableArguments {
    @Flag(name: [.customLong("content-table"), .customShort("c")], help: "Add a content table")
      var ct: Bool = false
    @Flag(name: .shortAndLong, help: "Add a navigation utility")
    var navigation: Bool = false
    @Flag(name: .long, help: "Includes file informations in the header if any")
    var infos: Bool = false

    @Option(name: .long, help: "Include an HTML header (path[*3]; HTML[,CSS,JS])")
    var header: [String] = []
    @Option(name: .long, help: "Include an HTML footer (path[*3]; HTML[,CSS,JS])")
    var footer: [String] = []
    @Option(name: .long, help: "Include an HTML email form (path[*3]; HTML[,CSS,JS])")
    var email: [String] = []

    struct mrsnippet: ExpressibleByArgument {
      var name: String
      var htmlfile: String
      var cssfile: String?
      var jsfile: String?

      init?(argument: String) {
        let components = argument.components(separatedBy: ",")
        guard components.count >= 2 else { return nil }
        name     = components[0]
        htmlfile = components[1]
        cssfile  = components.count > 2 ? components[2] : nil
        jsfile   = components.count > 3 ? components[3] : nil
      }
    }

    @Option(name: .customLong("snippet"), help: "Include a snippet where it is specified in the document with {&name}(`name,html,css,js`)")
    var snippets: [mrsnippet] = []

    @Flag(name: .long, help: "No tasklist script")
    var notlscript: Bool = false
  }

  struct expr {
    static let head = try!  NSRegularExpression(pattern: #"^(#+)\s+"#, options: [])
    static let tag = try! NSRegularExpression(pattern: #"^#(,?)(?<tag>\w+)"#, options: [])

    static let tl1 = try! NSRegularExpression(pattern: #"^-\s+\[(x|-| |&|\~|\+)\](?<hr>\s+-{3,}$)?"#, options: [])
    static let ul1 = try! NSRegularExpression(pattern: #"^-\s+(?<hr>-{3,}$)?"#, options: [])
    static let ol1 = try! NSRegularExpression(pattern: #"^(\d+)\.\s+(?<hr>-{3,}$)?"#, options: [])

    static let tl2 = try! NSRegularExpression(pattern: #"^(-+)\s+\[(x|-| |&|\~|\+)\](?<hr>\s+-{3,}$)?"#, options: [])
    static let ul2 = try! NSRegularExpression(pattern: #"^(-+)\s+(?<hr>-{3,}$)?"#, options: [])
    static let ol2 = try! NSRegularExpression(pattern: #"^(\d+)(\.+)\s+(?<hr>-{3,}$)?"#, options: [])

    static let rl = try!  NSRegularExpression(pattern: #"^\[(\w+)\]\:"#, options: [])

    // static let fc = try!  NSRegularExpression(pattern: #"^``"#, options: [])
    static let cbo = try! NSRegularExpression(pattern: #"^```\s*(?<lang>\w+)?$"#, options: [])
    static let cbc = try! NSRegularExpression(pattern: #"^((?<t>\s*)```\s*)"#, options: [])

    static let dbo = try! NSRegularExpression(pattern: #"^\({2}\s*(?<summary>.+)?$"#, options: [])
    static let dbc = try! NSRegularExpression(pattern: #"^\){2}"#, options: [])

    static let sbo = try! NSRegularExpression(pattern: #"^\{{2}"#, options: [])
    static let sbc = try! NSRegularExpression(pattern: #"^\}{2}"#, options: [])

    // grids...

    static let style = try! NSRegularExpression(pattern: #"(!!|\|{2}|\*{1,2}|==|__|~~|''|`|\^\^|,,"#, options: [])

    // links
    // static let wklnk = try!  NSRegularExpression(pattern: #"(?<img>\!)\[\[(?<data>)\]\]"#, options: [])
    static let link = try!  NSRegularExpression(pattern: #"(?<img>\!)?\[(?<txt>)\]\s*\((?<lnk>)\)"#, options: [])
    // clickable link
    // email
    // url

    // table ...

    static let quote = try! NSRegularExpression(pattern: #"(\>\s*)+((?<hr>-{3,}$)|(\~\s*(?<sn>.+$)))?"#, options: [])

    // static let annotation = try! NSRegularExpression(pattern: #"^{(?<annotation>(?<type>[%@~#&!^*])(?<param>[\w\d\-\+]+)(=(?<val>[\w\d\-\+]+))?){0}(\g<annotation>)(,(\g<annotation>))*}$"#, options: [])
    // ^{(?<annotation>(?<type>[%@~#&!^*])(?<param>[\w\d\-\+]+)(=(?<val>[\w\d\-\+]+))?)(,(\g<annotation>))*}$

    static let an_detect = try! NSRegularExpression(pattern: #"^{([%@~#&!^*\w\-\+\=,]+)}$"#, options: [])
    static let an_ident = try!  NSRegularExpression(pattern: #"(?<type>[%@~#&!^'*<=>:;])(?<param>[\w\d\-\+]+)(?<val>=[\w\d\-\+]*)?"#, options: [])

    static let misc = try!  NSRegularExpression(pattern: #"((?<susp>\.{3})|(?<dash>--)|(?<oq>\<\<)|(?<cq>\>\>)|(?<arr>->)|(?<arl><-)|(?<cc>\(c\))|(?<r>\(r\))|)"#, options: [])
    static let symb = try!  NSRegularExpression(pattern: #"\:(\w+)\:"#, options: [])
    static let escape = try! NSRegularExpression(pattern: #"\\((?<cancel>[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~])|(?<feature>n)|((?<not>\\)\s(?<styling>\w+)))"#, options: [])
    static let hr = try!  NSRegularExpression(pattern: #"^-{3,}$"#, options: [])

    static let roman = try! NSRegularExpression(pattern: #"(?<r1000>M{1,5}|(?<r900>CM))?((?<r600>DC{1,3})|(?<r500>D)|(?<r400>CD)|(?<r100>C{1,3})|(?<r90>XC))?((?<r60>LX{1,3})|(?<r50>L)|(?<r40>XL)|(?<r10>X{1,3})|(?<r9>IX))?((?<r6>VI{1,3})|(?<r5>V)|(?<r4>IV)|(?<r1>I{1,3}))?"#, options: [])

    // LaTeX
  }

  struct mrprod {
    struct ctobj {
      var headname: String
      var tag: String
      var type: Int
      // h1: 0 ... h6: 5
    }
    var ctable: [ctobj]?

    let styles = [
      // "!!": [false, <>]
      "||": [false, "<span class=\"half mr-half\">", "</span>"],
      "*":  [false, "<em>", "</em>"],
      "**": [false, "<strong>", "</strong>"],
      "==": [false, "<mark>", "</mark>"],
      "__": [false, "<ins>", "</ins>"],
      "~~": [false, "<strike>", "</strike>"],
      "''": [false, "<q>", "</q>"],
      "`":  [false, "<code>", "</code>"],
      "^^": [false, "<sup>", "</sup>"],
      ",,": [false, "<sub>", "</sub>"]
    ]
    var emptylines = 0
    var tabulation = 0

    struct anparam {
      let param: String
      let val: String?
    }
    var annotations: [String : [anparam]] = [
      "%": [], "@": [], "~": [], "#": [], "&": [], "!": [], "^": [],
      "'": [], "*": [], "<": [], "=": [], ">": [], ":": [], ";": []
    ]

    var lists: [String] = []
    var codeblocks = false
    var codeblang = ""
  }

  //  LOGIC FOR NEW LINES AND LINE JUMPS : MR-PAR-006
  // =====================================
  // - An empty line is a line break.
  // - two successive empty lines is/are paragraph cuts.
  // - more than two successive empty lines are line breaks
  // =====================================
  // +---------------[...]---------------+
  // | has proven it self to be rather   |
  // | difficult...                      |
  // |                                   |
  // | Alternatively, the creation of    |
  // +---------------[...]---------------+
  // Would give: ``[...] difficult...<br>Alternatively [...]``
  // =====================================
  // +---------------[...]---------------+
  // | The creation of standards remain  |
  // | the most efficient and versatile  |
  // | solution                          |
  // |                                   |
  // |                                   |
  // | In this search for universality   |
  // +---------------[...]---------------+
  // Would give: ``[...] difficult...</p><p>Alternatively [...]``

  func defaultNSRange(_ l: Int) -> NSRange {
    return NSRange(location: 0, length: l) }
  func getMatch(no i: Int, from m: NSTextCheckingResult, after s: String) -> String? {
    guard let rg = Range(m.range(at: i), in: s) else {
      return nil
    }
    let rt = String(s[rg.upperBound...])
    return rt
  }
  func getMatch(named n: String, from m: NSTextCheckingResult, after s: String) -> String? {
    if let nm = Range(m.range(withName: n), in: s) {
      return String(s[nm.upperBound...])
    }
    return nil
  }


  func parseline(_ _line: String, _ lnum: Int, _ prod: inout mrprod) -> Data {
    var ret = ""
    var tabs: Int
    var line: String

    if prod.codeblocks {
      if let m = expr.cbc.firstMatch(in: _line, options: [], range: defaultNSRange(_line.count)) {
        line = String(_line[
          _line.index(_line.startIndex, offsetBy: 0) ..<
          _line.index(_line.startIndex, offsetBy: getMatch(no: 1, from: m, after: _line)!.count)])
        tabs = (getMatch(named: "t", from: m, after: _line) ?? "").count

        ret += "</pre>"

        prod.codeblocks = false
      } else {
        // parsing code
        // ! Backslash features
        ret += _line
        return ret.data(using: .utf8) ?? Data()
      }
    }

    (tabs, line) = stripline(_line)

    // TODO: list closing (1v)
    if prod.tabulation == 0 { prod.tabulation = tabs }

    // TODO: list closing (2v)

    if line.count == 0 {
      prod.emptylines += 1

      return Data()
    } else {
      if prod.emptylines == 1 { ret += "<br>" }
      else if prod.emptylines == 2 { ret += "</p><p>" }
      else { ret += "</p>\(String(repeating: "<br>", count: prod.emptylines))<p>" }

      prod.emptylines = 0
    }

    if let _ = expr.hr.firstMatch(in: line, options: [], range: defaultNSRange(line.count)) {
      ret += "<hr>"
      return ret.data(using: .utf8) ?? Data()
    }

    if let m = expr.an_detect.firstMatch(in: line, options: [], range: defaultNSRange(line.count)) {
      let ans = getMatch(no: 1, from: m, after: line)!.components(separatedBy: ",")

      for (i, a) in ans.enumerated() {
        if let an = expr.an_ident.firstMatch(in: a, options: [], range: defaultNSRange(a.count)) {
          let t = getMatch(named: "type", from: an, after: a)!
          let pr = mrprod.anparam(
            param: getMatch(named: "param", from: an, after: a)!,
            val:   getMatch(named: "val", from: an, after: a))

          prod.annotations[t]?.append(pr)
        } else {
          print("error: annotation No \(i+1): '\(a)', on line \(line).")
          print("error: expression is not a valid annotation (MR-ANN-002)")
        }
      }

      return Data()
    }


    // ! After lists
    if let m = expr.cbo.firstMatch(in: line, options: [], range: defaultNSRange(line.count)) {
      let lang = getMatch(named: "lang", from: m, after: line) ?? "txt"
      prod.codeblocks = true
      prod.codeblang = lang
      ret += "<pre class=\"codeblock mr-codeblock lang-\(lang)\" data-lang=\"lang\">"

      return ret.data(using: .utf8) ?? Data()
    }

    return ret.data(using: .utf8) ?? Data()
  }



  func stripline(_ line: String) -> (Int, String) {
    do {
      let ws = try NSRegularExpression(pattern: #"^(\s*)"#, options: [])
      if let m = ws.firstMatch(in: line, options: [], range: defaultNSRange(line.count)) {
        let wsr = Range(m.range(at: 1), in: line)!

        let wsc = wsr.upperBound.utf16Offset(in: line)
        let nl = String(line[wsr.upperBound...])

        return (wsc, nl)
      }
    } catch { print("Error creating regex") }

    return (0, line)
  }
}

mr.main()
