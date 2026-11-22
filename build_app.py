import json
import base64

with open('template_front.jpg', 'rb') as f:
    front_b64 = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

with open('template_back.jpg', 'rb') as f:
    back_b64 = 'data:image/jpeg;base64,' + base64.b64encode(f.read()).decode('utf-8')

print(f"Loaded front_b64 ({len(front_b64)} chars) and back_b64 ({len(back_b64)} chars)")

html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>ID Card Studio - Tech Area Pass (AFS Sulur)</title>
  <style>
    :root {{
      --primary: #2563eb;
      --primary-hover: #1d4ed8;
      --primary-light: #eff6ff;
      --surface: #ffffff;
      --bg: #f8fafc;
      --border: #e2e8f0;
      --border-dark: #cbd5e1;
      --text: #0f172a;
      --text-muted: #64748b;
      --danger: #ef4444;
      --danger-hover: #dc2626;
      --success: #16a34a;
      --success-hover: #15803d;
      --font: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}

    * {{ box-sizing: border-box; font-family: var(--font); margin: 0; padding: 0; }}
    body {{ background: var(--bg); color: var(--text); height: 100vh; display: flex; flex-direction: column; overflow: hidden; }}

    /* Header Bar */
    .header {{
      height: 52px; background: #0f172a; color: #ffffff;
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 16px; border-bottom: 1px solid #1e293b; z-index: 20; flex-shrink: 0;
    }}
    .header-left {{ display: flex; align-items: center; gap: 12px; }}
    .header-title {{ font-size: 15px; font-weight: 700; letter-spacing: 0.02em; display: flex; align-items: center; gap: 8px; }}
    .badge {{
      background: #1e293b; color: #94a3b8; font-size: 11px; padding: 2px 8px;
      border-radius: 999px; border: 1px solid #334155; font-weight: 500;
    }}
    .badge.green {{ background: rgba(22, 163, 74, 0.2); color: #4ade80; border-color: rgba(22, 163, 74, 0.4); }}
    .badge.blue {{ background: rgba(37, 99, 235, 0.2); color: #60a5fa; border-color: rgba(37, 99, 235, 0.4); }}
    .header-actions {{ display: flex; align-items: center; gap: 8px; }}

    /* Buttons */
    button, .btn {{
      display: inline-flex; align-items: center; justify-content: center; gap: 6px;
      padding: 6px 12px; border-radius: 6px; font-size: 12px; font-weight: 600;
      cursor: pointer; transition: all 0.15s ease; border: 1px solid transparent;
      outline: none; white-space: nowrap; text-decoration: none;
    }}
    button.btn-primary {{ background: var(--primary); color: #fff; }}
    button.btn-primary:hover {{ background: var(--primary-hover); }}
    button.btn-success {{ background: var(--success); color: #fff; }}
    button.btn-success:hover {{ background: var(--success-hover); }}
    button.btn-secondary {{ background: #ffffff; color: var(--text); border-color: var(--border-dark); }}
    button.btn-secondary:hover {{ background: #f1f5f9; }}
    button.btn-dark {{ background: #1e293b; color: #f8fafc; border-color: #334155; }}
    button.btn-dark:hover {{ background: #334155; }}
    button.btn-danger {{ background: var(--danger); color: #fff; }}
    button.btn-danger:hover {{ background: var(--danger-hover); }}
    button.btn-sm {{ padding: 4px 8px; font-size: 11px; }}
    button.btn-xs {{ padding: 3px 7px; font-size: 11px; border-radius: 4px; }}
    button.btn-icon {{ padding: 6px; width: 30px; height: 30px; border-radius: 6px; }}

    /* Layout Structure */
    .app-workspace {{ flex: 1; display: flex; overflow: hidden; position: relative; }}
    
    /* Sidebar */
    .sidebar {{
      width: 460px; background: var(--surface); border-right: 1px solid var(--border);
      display: flex; flex-direction: column; overflow: hidden; flex-shrink: 0;
    }}
    
    /* Person Switcher Bar */
    .person-toolbar {{
      padding: 10px 14px; background: #f8fafc; border-bottom: 1px solid var(--border);
      display: flex; align-items: center; gap: 8px;
    }}
    .person-select-wrapper {{ flex: 1; position: relative; }}
    select.person-select {{
      width: 100%; padding: 6px 10px; font-size: 12px; font-weight: 600;
      border: 1px solid var(--border-dark); border-radius: 6px; background: #fff;
      color: var(--text); cursor: pointer;
    }}
    
    /* Sidebar Navigation Tabs */
    .sidebar-tabs {{
      display: flex; border-bottom: 1px solid var(--border); background: #f8fafc;
    }}
    .sidebar-tab {{
      flex: 1; padding: 9px 8px; font-size: 12px; font-weight: 600;
      text-align: center; color: var(--text-muted); cursor: pointer;
      border-bottom: 2px solid transparent; background: transparent; border-radius: 0;
    }}
    .sidebar-tab.active {{
      color: var(--primary); border-bottom-color: var(--primary); background: #ffffff;
    }}

    /* Sidebar Scrollable Body */
    .sidebar-body {{ flex: 1; overflow-y: auto; padding: 14px; display: flex; flex-direction: column; gap: 14px; }}
    
    /* Section Cards */
    .card-section {{
      background: #ffffff; border: 1px solid var(--border); border-radius: 8px;
      padding: 12px; display: flex; flex-direction: column; gap: 10px;
    }}
    .section-title {{
      font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em;
      color: #475569; display: flex; align-items: center; justify-content: space-between;
    }}
    
    /* Edit Mode Banner */
    .edit-banner {{
      display: flex; align-items: center; justify-content: space-between;
      padding: 8px 12px; border-radius: 6px; background: #f1f5f9; border: 1px solid var(--border-dark);
      font-size: 12px; font-weight: 600; color: #334155;
    }}
    .edit-banner.unlocked {{
      background: #eff6ff; border-color: #93c5fd; color: #1e40af;
    }}
    
    /* Form Inputs */
    .field-row {{ display: flex; gap: 8px; align-items: center; }}
    .field-col {{ display: flex; flex-direction: column; gap: 4px; flex: 1; }}
    label.input-label {{ font-size: 11px; font-weight: 600; color: #475569; display: flex; justify-content: space-between; }}
    
    /* SPATIOUS, CLEAR FIELD CARD DESIGN */
    .field-entry-card {{
      background: #f8fafc; border: 1px solid #cbd5e1; border-radius: 8px;
      padding: 10px; display: flex; flex-direction: column; gap: 6px;
      box-shadow: 0 1px 2px rgba(0,0,0,0.03); transition: border-color 0.15s;
    }}
    .field-entry-card:focus-within {{
      border-color: var(--primary); background: #ffffff;
    }}
    .field-entry-header {{
      display: flex; justify-content: space-between; align-items: center;
    }}
    .field-label-wrapper {{
      display: flex; align-items: center; gap: 6px; flex: 1; min-width: 0;
    }}
    .field-tag-badge {{
      font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
      background: #e2e8f0; color: #475569; padding: 1px 6px; border-radius: 4px;
    }}
    .field-name-text {{
      font-size: 13px; font-weight: 700; color: #0f172a; border: 1px solid transparent;
      background: transparent; padding: 2px 4px; border-radius: 4px; max-width: 180px;
    }}
    .field-name-text:hover, .field-name-text:focus {{
      border-color: #94a3b8; background: #ffffff; outline: none;
    }}
    
    /* LARGE, HIGH-CONTRAST VALUE INPUT */
    .field-value-input-large {{
      width: 100% !important; box-sizing: border-box !important;
      padding: 9px 12px !important; font-size: 14px !important; font-weight: 600 !important;
      border: 1.5px solid #cbd5e1 !important; border-radius: 6px !important;
      background: #ffffff !important; color: #0f172a !important;
      outline: none !important; transition: border-color 0.15s, box-shadow 0.15s !important;
    }}
    .field-value-input-large:focus {{
      border-color: var(--primary) !important;
      box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.18) !important;
    }}
    
    /* Main Center Stage */
    .main-stage {{
      flex: 1; background: #e2e8f0; display: flex; flex-direction: column;
      position: relative; overflow: hidden;
    }}
    .stage-toolbar {{
      height: 48px; background: #ffffff; border-bottom: 1px solid var(--border);
      display: flex; align-items: center; justify-content: space-between;
      padding: 0 16px; flex-shrink: 0;
    }}
    .side-tabs {{ display: flex; gap: 6px; }}
    .side-tab-btn {{
      padding: 6px 14px; border-radius: 6px; font-size: 12px; font-weight: 600;
      background: #f1f5f9; color: var(--text-muted); border: 1px solid var(--border);
    }}
    .side-tab-btn.active {{
      background: #0f172a; color: #ffffff; border-color: #0f172a;
    }}
    .zoom-controls {{ display: flex; align-items: center; gap: 6px; font-size: 12px; font-weight: 600; }}
    
    /* Canvas Container */
    .canvas-viewport {{
      flex: 1; overflow: auto; display: flex; align-items: center; justify-content: center;
      padding: 24px; position: relative;
    }}
    canvas#cardCanvas {{
      background: #ffffff; box-shadow: 0 10px 30px rgba(0,0,0,0.15);
      border-radius: 8px; cursor: default; max-width: 95%; max-height: 82vh; object-fit: contain;
    }}
    body.layout-unlocked canvas#cardCanvas {{ cursor: grab; }}
    body.layout-unlocked canvas#cardCanvas:active {{ cursor: grabbing; }}

    /* MODERN FLOATING INLINE TEXT TOOLBAR */
    .floating-toolbar {{
      position: absolute; display: none; align-items: center; gap: 8px;
      background: #0f172a; color: #ffffff; padding: 6px 12px; border-radius: 8px;
      box-shadow: 0 12px 28px rgba(0,0,0,0.3); z-index: 50; transform: translate(-50%, -100%);
      margin-top: -10px; font-size: 12px; pointer-events: auto; animation: popIn 0.15s ease-out;
    }}
    .floating-toolbar.open {{ display: flex; }}
    @keyframes popIn {{ from {{ opacity: 0; transform: translate(-50%, -90%); }} to {{ opacity: 1; transform: translate(-50%, -100%); }} }}
    .ft-label {{ font-size: 11px; font-weight: 700; color: #94a3b8; text-transform: uppercase; }}
    .ft-input {{
      background: #1e293b; border: 1px solid #334155; color: #fff; padding: 4px 8px;
      border-radius: 4px; font-size: 12px; font-weight: 600; min-width: 140px; outline: none;
    }}
    .ft-input:focus {{ border-color: var(--primary); }}
    .ft-btn {{
      background: #1e293b; border: 1px solid #334155; color: #fff; padding: 3px 8px;
      border-radius: 4px; cursor: pointer; font-size: 11px; font-weight: 700;
    }}
    .ft-btn:hover {{ background: #334155; }}
    .ft-btn-toggle {{
      background: #1e293b; border: 1px solid #334155; color: #fff; padding: 3px 8px;
      border-radius: 4px; cursor: pointer; font-size: 11px; font-weight: 700;
    }}
    .ft-btn-toggle.active {{ background: var(--primary); border-color: var(--primary); }}
    .ft-divider {{ width: 1px; height: 18px; background: #334155; }}
    .ft-color {{
      width: 24px; height: 24px; border: 1px solid #334155; border-radius: 4px;
      padding: 0; cursor: pointer; background: transparent;
    }}

    /* Modal Dialogs */
    .modal-backdrop {{
      position: fixed; inset: 0; background: rgba(15, 23, 42, 0.6);
      backdrop-filter: blur(4px); z-index: 100; display: none;
      align-items: center; justify-content: center; padding: 20px;
    }}
    .modal-backdrop.open {{ display: flex; }}
    .modal-container {{
      background: #ffffff; border-radius: 12px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      max-width: 95vw; max-height: 90vh; display: flex; flex-direction: column; overflow: hidden;
    }}
    .modal-header {{
      padding: 12px 20px; background: #0f172a; color: #ffffff;
      display: flex; align-items: center; justify-content: space-between;
    }}
    .modal-title {{ font-size: 14px; font-weight: 700; display: flex; align-items: center; gap: 8px; }}
    .modal-body {{ flex: 1; overflow-y: auto; padding: 16px; }}
    .modal-footer {{
      padding: 12px 20px; background: #f8fafc; border-top: 1px solid var(--border);
      display: flex; justify-content: flex-end; gap: 10px;
    }}

    /* Bulk Edit Table */
    .table-responsive {{ overflow-x: auto; max-height: 65vh; }}
    table.data-table {{
      width: 100%; border-collapse: collapse; font-size: 13px;
    }}
    table.data-table th {{
      background: #f1f5f9; padding: 9px 12px; text-align: left; font-weight: 700;
      color: #334155; border: 1px solid var(--border); position: sticky; top: 0; z-index: 5;
    }}
    table.data-table td {{
      padding: 6px 8px; border: 1px solid var(--border); background: #ffffff;
    }}
    table.data-table tr:hover td {{ background: #f8fafc; }}
    table.data-table input[type="text"] {{
      border: 1px solid transparent; background: transparent; padding: 6px 8px; width: 100%;
      font-size: 13px; font-weight: 600; color: #0f172a;
    }}
    table.data-table input[type="text"]:focus {{
      border-color: var(--primary); background: #ffffff; box-shadow: 0 0 0 2px rgba(37,99,235,0.15);
    }}
    .photo-thumb-cell {{
      width: 44px; height: 44px; position: relative; display: flex; align-items: center; justify-content: center;
      background: #f1f5f9; border-radius: 4px; overflow: hidden; border: 1px solid var(--border); cursor: pointer;
    }}
    .photo-thumb-cell img {{ width: 100%; height: 100%; object-fit: cover; }}

    /* Print Preview & Print Styles */
    .print-preview-container {{
      background: #334155; padding: 20px; display: flex; flex-direction: column;
      align-items: center; gap: 20px; overflow-y: auto; max-height: 70vh;
    }}
    .virtual-a4-page {{
      background: #ffffff; width: 210mm; min-height: 297mm; padding: 10mm 15mm;
      box-shadow: 0 10px 25px rgba(0,0,0,0.3); display: flex; flex-direction: column;
      align-items: center; box-sizing: border-box; position: relative;
    }}
    .virtual-print-row {{
      display: flex; flex-direction: row; justify-content: center; align-items: center;
      margin-bottom: 5mm; position: relative; page-break-inside: avoid; break-inside: avoid;
    }}
    .virtual-print-card {{
      width: 80mm; height: 45mm; object-fit: fill; position: relative;
      background: #fff; box-sizing: border-box;
    }}
    .cut-guide-dashed {{ border: 0.5px dashed #94a3b8 !important; }}
    .cut-guide-solid {{ border: 0.5px solid #cbd5e1 !important; }}

    /* PRINT MEDIA SPECIFIC RULES */
    @media print {{
      @page {{
        size: A4 portrait;
        margin: 10mm 15mm;
      }}
      body, html {{
        background: #ffffff !important;
        height: auto !important;
        overflow: visible !important;
      }}
      .no-print, .header, .sidebar, .main-stage, .modal-backdrop, .floating-toolbar {{
        display: none !important;
      }}
      #printContainer {{
        display: block !important;
        position: static !important;
        width: 100% !important;
        background: #ffffff !important;
        margin: 0 !important;
        padding: 0 !important;
      }}
      .print-a4-page {{
        width: 100% !important;
        min-height: 270mm !important;
        page-break-after: always !important;
        break-after: page !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: flex-start !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 auto !important;
      }}
      .print-row {{
        display: flex !important;
        flex-direction: row !important;
        justify-content: center !important;
        align-items: center !important;
        margin-bottom: 5mm !important;
        page-break-inside: avoid !important;
        break-inside: avoid !important;
      }}
      .print-card-img {{
        width: 80mm !important;
        height: 45mm !important;
        object-fit: fill !important;
        display: block !important;
      }}
    }}
    
    #printContainer {{ display: none; }}
  </style>
</head>
<body>

  <!-- Top Navigation Bar (Clean & Focused) -->
  <header class="header no-print">
    <div class="header-left">
      <div class="header-title">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><line x1="15" y1="8" x2="17" y2="8"/><line x1="15" y1="12" x2="17" y2="12"/><line x1="7" y1="16" x2="17" y2="16"/></svg>
        <span>ID Card Studio</span>
      </div>
      <span class="badge blue">Tech Area Pass - AFS Sulur</span>
      <span class="badge green" id="peopleCountBadge">3 People</span>
      <span class="badge">A4 Card Size: 8.0 × 4.5 cm</span>
    </div>
    <div class="header-actions">
      <button class="btn btn-secondary btn-sm" onclick="openBulkEditModal()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h18v18H3zM3 9h18M9 3v18"/></svg>
        Spreadsheet View
      </button>
      <button class="btn btn-success" onclick="openPrintModal()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
        Print Cards (A4)
      </button>
    </div>
  </header>

  <!-- Workspace Structure -->
  <div class="app-workspace no-print">
    
    <!-- Sidebar -->
    <aside class="sidebar">
      
      <!-- Person Selector & Switcher -->
      <div class="person-toolbar">
        <button class="btn btn-secondary btn-icon" title="Previous Person" onclick="navigatePerson(-1)">◀</button>
        <div class="person-select-wrapper">
          <select id="personSelect" class="person-select" onchange="selectPerson(+this.value)"></select>
        </div>
        <button class="btn btn-secondary btn-icon" title="Next Person" onclick="navigatePerson(1)">▶</button>
        <button class="btn btn-primary btn-sm" title="Add New Person" onclick="addNewPerson()">+ Add</button>
        <button class="btn btn-secondary btn-sm" title="Duplicate Person" onclick="duplicateCurrentPerson()">Copy</button>
        <button class="btn btn-danger btn-sm" title="Delete Person" onclick="deleteCurrentPerson()">×</button>
      </div>

      <!-- Navigation Tabs inside Sidebar -->
      <div class="sidebar-tabs">
        <button class="sidebar-tab active" id="tabBtnDetails" onclick="switchSidebarTab('details')">1. Card Data</button>
        <button class="sidebar-tab" id="tabBtnLayout" onclick="switchSidebarTab('layout')">2. Layout & Style</button>
        <button class="sidebar-tab" id="tabBtnPrint" onclick="switchSidebarTab('print')">3. Print & Size</button>
      </div>

      <!-- Scrollable Content -->
      <div class="sidebar-body">
        
        <!-- ================= TAB 1: CARD DATA ================= -->
        <div id="tabDetails" style="display: flex; flex-direction: column; gap: 14px;">
          
          <!-- Side Selector Indicator inside Sidebar -->
          <div style="display: flex; gap: 6px; background: #f1f5f9; padding: 4px; border-radius: 8px;">
            <button id="btnSideToggleFront" class="btn btn-sm" style="flex: 1; background: #0f172a; color: #fff;" onclick="switchSide('front')">Front Side Data</button>
            <button id="btnSideToggleBack" class="btn btn-sm" style="flex: 1; background: transparent; color: #475569;" onclick="switchSide('back')">Back Side Data</button>
          </div>

          <!-- FRONT SIDE SECTIONS -->
          <div id="frontSideDataSection" style="display: flex; flex-direction: column; gap: 14px;">
            
            <!-- Front Photo Card with Pan & Zoom -->
            <div class="card-section">
              <div class="section-title">
                <span>Standard Passport Photo (3.5 × 4.5)</span>
                <div style="display: flex; gap: 4px;">
                  <button class="btn btn-secondary btn-xs" onclick="resetPhotoPosition()" title="Reset photo pan and zoom">Reset Position</button>
                  <button class="btn btn-danger btn-xs" onclick="clearCurrentPhoto()">Clear Photo</button>
                </div>
              </div>
              
              <input type="file" id="personPhotoInput" accept="image/*" onchange="uploadPersonPhoto(event)" style="font-size: 11px;" />
              
              <!-- Photo Pan & Zoom Controls -->
              <div style="background: #f8fafc; border: 1px solid var(--border); border-radius: 6px; padding: 8px; display: flex; flex-direction: column; gap: 6px;">
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 11px; font-weight: 600; color: #475569;">
                  <span>Photo Zoom: <span id="photoZoomText">100%</span></span>
                  <div style="display: flex; gap: 4px;">
                    <button class="btn btn-secondary btn-xs" onclick="adjustPhotoZoom(-0.1)">-</button>
                    <button class="btn btn-secondary btn-xs" onclick="adjustPhotoZoom(0.1)">+</button>
                  </div>
                </div>
                <input type="range" id="photoZoomSlider" min="0.5" max="3.0" step="0.05" value="1.0" oninput="setPhotoZoom(+this.value)" style="width: 100%; cursor: pointer;" />
                <div class="hint" style="font-size: 11px; color: #2563eb; font-weight: 600;">
                  💡 Click & drag photo directly on the card to center face
                </div>
              </div>
            </div>

            <!-- Front Text Fields (PP No, Name, Designation, Country, Validity) -->
            <div class="card-section">
              <div class="section-title">
                <span>Front Fields & Values</span>
                <div style="display: flex; gap: 4px;">
                  <button class="btn btn-outline btn-xs" onclick="resetDefaultFields('front')" title="Reset to standard default front fields">↺ Reset Defaults</button>
                  <button class="btn btn-primary btn-sm" onclick="addNewField('front')">+ Add Field</button>
                </div>
              </div>
              <div id="frontFieldsList" style="display: flex; flex-direction: column; gap: 10px;">
                <!-- Dynamic spacious field cards injected here -->
              </div>
            </div>

          </div>

          <!-- BACK SIDE SECTIONS -->
          <div id="backSideDataSection" style="display: none; flex-direction: column; gap: 14px;">
            
            <div class="card-section">
              <div class="section-title">
                <span>Top & Middle Back Fields</span>
                <div style="display: flex; gap: 4px;">
                  <button class="btn btn-outline btn-xs" onclick="resetDefaultFields('back')" title="Reset to standard default back fields">↺ Reset Defaults</button>
                  <button class="btn btn-secondary btn-sm" onclick="applyCommonBackValuesToAll()" title="Apply Validity & Date to all people">Copy to All</button>
                  <button class="btn btn-primary btn-sm" onclick="addNewField('back')">+ Add Field</button>
                </div>
              </div>
              <div id="backFieldsList" style="display: flex; flex-direction: column; gap: 10px;">
                <!-- Dynamic spacious back fields injected here -->
              </div>
            </div>

            <div class="card-section">
              <div class="section-title">
                <span>Signature Line & Date</span>
                <button class="btn btn-secondary btn-sm" onclick="clearAuthoritySign()">Clear Sign</button>
              </div>
              <div class="field-col">
                <label class="input-label">Date</label>
                <input type="text" id="backDateInput" class="form-input" style="padding: 8px 12px; font-size: 14px; font-weight: 600; border: 1.5px solid #cbd5e1; border-radius: 6px;" oninput="updateBackDate(this.value)" />
              </div>
              <div class="field-col" style="margin-top: 6px;">
                <label class="input-label">Upload Authority Signature / Stamp (Optional)</label>
                <input type="file" id="authoritySignInput" accept="image/*" onchange="uploadAuthoritySign(event)" style="font-size: 11px;" />
              </div>
            </div>

            <div class="card-section">
              <div class="section-title">
                <span>Numbered Terms (Editable Paragraphs)</span>
              </div>
              <div id="backTermsList" style="display: flex; flex-direction: column; gap: 8px;">
                <!-- Editable Terms -->
              </div>
            </div>

          </div>

        </div>

        <!-- ================= TAB 2: LAYOUT & STYLE ================= -->
        <div id="tabLayout" style="display: none; flex-direction: column; gap: 14px;">
          
          <!-- Layout Lock / Unlock Toggle -->
          <div id="editBanner" class="edit-banner">
            <label style="display: flex; align-items: center; gap: 8px; cursor: pointer; margin: 0;">
              <input type="checkbox" id="layoutLockToggle" onchange="toggleLayoutMode(this.checked)" />
              <span>Enable Layout Drag & Reposition</span>
            </label>
            <span id="lockStatusBadge" class="badge">LOCKED</span>
          </div>

          <!-- Middle Logo Fade / Watermark Slider -->
          <div class="card-section" id="logoFadeCard">
            <div class="section-title">
              <span>Middle Logo Watermark Fade</span>
              <span id="logoFadeValueText" style="font-size: 11px; font-weight: 700; color: #2563eb;">82% Faded</span>
            </div>
            <div class="field-col">
              <input type="range" id="cfgLogoFade" min="0" max="100" step="2" value="82" oninput="updateLogoFade(+this.value)" style="width: 100%; cursor: pointer;" />
              <div style="display: flex; justify-content: space-between; font-size: 10px; color: var(--text-muted);">
                <span>0% (Original Dark)</span>
                <span>82% (Recommended)</span>
                <span>100% (White)</span>
              </div>
            </div>
            <div class="hint" style="font-size: 11px; color: var(--text-muted);">
              Fades the center emblem so all text printed over it is sharp and crystal clear.
            </div>
          </div>

          <!-- Profile Photo Frame Size Settings -->
          <div class="card-section">
            <div class="section-title">
              <span>Photo Box Size (Standard Card)</span>
              <button class="btn btn-secondary btn-sm" onclick="resetPhotoBoxToStandard()">Standard Size</button>
            </div>
            <div class="field-row">
              <div class="field-col">
                <label class="input-label">Width (px)</label>
                <input type="number" id="cfgPhotoW" class="form-input" onchange="updatePhotoBox('w', +this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
              <div class="field-col">
                <label class="input-label">Height (px)</label>
                <input type="number" id="cfgPhotoH" class="form-input" onchange="updatePhotoBox('h', +this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
            </div>
            <div class="hint" style="font-size: 11px; color: var(--text-muted);">
              Standard 270 × 350 px matches official 3.5 × 4.5 cm passport proportions.
            </div>
          </div>

          <!-- Front Text Formatting & Dotted Line Style -->
          <div class="card-section" id="frontLayoutCard">
            <div class="section-title">
              <span>Front Text & Layout</span>
            </div>

            <div class="field-col">
              <label class="input-label">Format Style</label>
              <select id="dotStyleSelect" class="form-input" onchange="updateTextConfig('dotStyle', this.value)" style="padding: 7px 8px; font-size: 12px; border: 1px solid var(--border-dark); border-radius: 6px;">
                <option value="clean" selected>Clean Colon: No Dots (PA No. : 123456) [Default]</option>
                <option value="colon-dots">Colon + Trailing Dots (PA No. : 123456 . . . .)</option>
                <option value="dots-nearby">Dots + Trailing Dots (PA No. . . 123456 . . . .)</option>
                <option value="leader">Leader Dots (PA No. . . . . . . . 123456)</option>
                <option value="value-on-dots">Value on Continuous Dotted Line</option>
              </select>
            </div>

            <div class="field-row">
              <div class="field-col">
                <label class="input-label">Start X (Left)</label>
                <input type="number" id="cfgStartX" class="form-input" onchange="updateTextConfig('startX', +this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
              <div class="field-col">
                <label class="input-label">Start Y (Top)</label>
                <input type="number" id="cfgStartY" class="form-input" onchange="updateTextConfig('startY', +this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
            </div>

            <div class="field-row">
              <div class="field-col">
                <label class="input-label">Line Spacing (Row Gap)</label>
                <input type="number" id="cfgRowGap" class="form-input" onchange="updateTextConfig('rowGap', +this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
              <div class="field-col">
                <label class="input-label">Label Width (Colon Align)</label>
                <input type="number" id="cfgLabelWidth" class="form-input" onchange="updateTextConfig('labelWidth', +this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
            </div>

            <div class="field-row">
              <div class="field-col">
                <label class="input-label">Font Size (px)</label>
                <input type="number" id="cfgFontSize" class="form-input" onchange="updateTextConfig('fontSize', +this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
              <div class="field-col">
                <label class="input-label">Value Text Color</label>
                <input type="color" id="cfgValueColor" style="width: 100%; height: 32px; border: 1px solid var(--border-dark); border-radius: 6px; padding: 2px;" onchange="updateTextConfig('valueColor', this.value)" />
              </div>
            </div>

            <div class="field-row" style="margin-top: 4px;">
              <label style="display: flex; align-items: center; gap: 8px; font-size: 12px; cursor: pointer;">
                <input type="checkbox" id="cfgBold" onchange="updateTextConfig('bold', this.checked)" />
                <span>Bold Text</span>
              </label>
            </div>
          </div>

          <!-- Template Background Uploads (Optional) -->
          <div class="card-section">
            <div class="section-title">
              <span>Custom Background Images (Optional)</span>
            </div>
            <div class="field-col">
              <label class="input-label">Change Front Card Image</label>
              <input type="file" accept="image/*" onchange="changeCustomBg(event, 'front')" style="font-size: 11px;" />
            </div>
            <div class="field-col">
              <label class="input-label">Change Back Card Image</label>
              <input type="file" accept="image/*" onchange="changeCustomBg(event, 'back')" style="font-size: 11px;" />
            </div>
            <button class="btn btn-secondary btn-sm" onclick="resetDefaultBackgrounds()">Restore Default Templates</button>
          </div>

        </div>

        <!-- ================= TAB 3: PRINT & CARD SIZE ================= -->
        <div id="printTabContent" style="display: none; flex-direction: column; gap: 14px;">
          <div class="card-section">
            <div class="section-title">
              <span>Card Dimensions & Lamination Margin</span>
            </div>
            <div class="field-row">
              <div class="field-col">
                <label class="input-label">Card Width (cm)</label>
                <input type="number" step="0.1" id="cfgCardWidth" class="form-input" value="8.0" onchange="updatePrintConfig('cardWidthMm', +this.value * 10)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
              <div class="field-col">
                <label class="input-label">Card Height (cm)</label>
                <input type="number" step="0.1" id="cfgCardHeight" class="form-input" value="4.5" onchange="updatePrintConfig('cardHeightMm', +this.value * 10)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
            </div>
            <div class="hint" style="font-size: 11px; color: var(--text-muted);">
              Standard 8.0 × 4.5 cm leaves clean border margin inside standard lamination pouches.
            </div>
          </div>

          <div class="card-section">
            <div class="section-title">
              <span>Multi-Person A4 Print Arrangement</span>
            </div>
            <div class="field-col">
              <label class="input-label">Print Format</label>
              <select id="cfgPrintMode" class="form-input" onchange="updatePrintConfig('printMode', this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;">
                <option value="both">Side-by-Side: Front + Back per person (5 cards/A4)</option>
                <option value="front-only">Fronts Only (10 cards/A4)</option>
                <option value="back-only">Backs Only (10 cards/A4)</option>
              </select>
            </div>
            <div class="field-row">
              <div class="field-col">
                <label class="input-label">Front/Back Gap (mm)</label>
                <input type="number" id="cfgPrintGap" class="form-input" value="4" onchange="updatePrintConfig('printGapMm', +this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
              <div class="field-col">
                <label class="input-label">Row Spacing (mm)</label>
                <input type="number" id="cfgPrintRowGap" class="form-input" value="5" onchange="updatePrintConfig('printRowGapMm', +this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;" />
              </div>
            </div>
            <div class="field-col">
              <label class="input-label">Scissor / Cutting Guide</label>
              <select id="cfgCutGuide" class="form-input" onchange="updatePrintConfig('cutGuide', this.value)" style="padding: 6px 8px; border: 1px solid var(--border-dark); border-radius: 6px;">
                <option value="dashed">Dashed Outline (Easy scissor cutting)</option>
                <option value="solid">Hairline Solid Border</option>
                <option value="none">Borderless</option>
              </select>
            </div>
            <button class="btn btn-success" style="width: 100%; margin-top: 6px;" onclick="openPrintModal()">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
              Open Print Preview & Print
            </button>
          </div>
        </div>

      </div>
    </aside>

    <!-- Main Stage Canvas -->
    <main class="main-stage">
      
      <!-- Stage Toolbar -->
      <div class="stage-toolbar">
        <div class="side-tabs">
          <button id="btnSideFront" class="side-tab-btn active" onclick="switchSide('front')">Front Side</button>
          <button id="btnSideBack" class="side-tab-btn" onclick="switchSide('back')">Back Side</button>
        </div>

        <div style="font-size: 12px; font-weight: 700; color: #334155;" id="currentCardTitle">
          Viewing: Person 1 (Front)
        </div>

        <div class="zoom-controls">
          <button class="btn btn-secondary btn-icon" title="Zoom Out" onclick="adjustZoom(-0.1)">-</button>
          <span id="zoomLevelText" style="min-width: 40px; text-align: center;">100%</span>
          <button class="btn btn-secondary btn-icon" title="Zoom In" onclick="adjustZoom(0.1)">+</button>
          <button class="btn btn-secondary btn-sm" onclick="resetZoom()">Fit</button>
        </div>
      </div>

      <!-- Canvas Viewport -->
      <div class="canvas-viewport" id="canvasViewport">
        <canvas id="cardCanvas" width="1024" height="764"></canvas>

        <!-- MODERN FLOATING INLINE TEXT TOOLBAR -->
        <div id="floatingToolbar" class="floating-toolbar">
          <span class="ft-label" id="ftFieldLabel">TEXT:</span>
          <input type="text" id="ftTextInput" class="ft-input" oninput="onFloatingTextChange(this.value)" />
          <div class="ft-divider"></div>
          <span class="ft-label">SIZE:</span>
          <button class="ft-btn" onclick="adjustFloatingSize(-2)">-</button>
          <span id="ftSizeText" style="font-weight:700; font-size:11px; min-width:20px; text-align:center;">28</span>
          <button class="ft-btn" onclick="adjustFloatingSize(2)">+</button>
          <div class="ft-divider"></div>
          <button id="ftBoldBtn" class="ft-btn-toggle" title="Toggle Bold" onclick="toggleFloatingBold()"><b>B</b></button>
          <input type="color" id="ftColorInput" class="ft-color" title="Change Color" onchange="updateFloatingColor(this.value)" />
          <div class="ft-divider"></div>
          <button class="btn btn-secondary btn-xs" style="padding: 2px 7px; font-size: 11px;" title="Hide this field on card" onclick="hideFloatingSelectedItem()">Hide</button>
          <button class="btn btn-primary btn-xs" onclick="closeFloatingToolbar()">Done</button>
        </div>

      </div>

      <!-- Quick Action Footer -->
      <div style="height: 42px; background: #ffffff; border-top: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; padding: 0 16px;">
        <div style="font-size: 11px; color: var(--text-muted);" id="stageHint">
          💡 Click any text on the card to edit with the modern floating toolbar. Drag photo to center face.
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-secondary btn-sm" onclick="downloadCurrentPNG('front')">Download Front PNG</button>
          <button class="btn btn-secondary btn-sm" onclick="downloadCurrentPNG('back')">Download Back PNG</button>
        </div>
      </div>

    </main>

  </div>

  <!-- ================= MODAL: SPREADSHEET / BULK EDIT ================= -->
  <div class="modal-backdrop no-print" id="bulkEditModal">
    <div class="modal-container" style="width: 1250px;">
      <div class="modal-header">
        <div class="modal-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3h18v18H3zM3 9h18M9 3v18"/></svg>
          <span>Spreadsheet Editor (All People in One Table)</span>
        </div>
        <button class="btn btn-dark btn-icon" onclick="closeBulkEditModal()">×</button>
      </div>
      <div class="modal-body">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
          <div style="display: flex; gap: 8px;">
            <button class="btn btn-primary btn-sm" onclick="addNewPersonFromModal()">+ Add Person</button>
            <button class="btn btn-secondary btn-sm" onclick="addMultiplePeopleFromModal(5)">+ Add 5 People</button>
            <button class="btn btn-secondary btn-sm" onclick="exportCSV()">Export CSV</button>
            <button class="btn btn-secondary btn-sm" onclick="document.getElementById('csvFileInput').click()">Import CSV</button>
            <input type="file" id="csvFileInput" accept=".csv" style="display:none;" onchange="importCSV(event)" />
          </div>
          <div style="font-size: 12px; color: var(--text-muted);">
            Type directly into any cell below. All changes apply across cards immediately.
          </div>
        </div>
        <div class="table-responsive">
          <table class="data-table" id="bulkTable">
            <thead>
              <tr id="bulkTableHead"></tr>
            </thead>
            <tbody id="bulkTableBody"></tbody>
          </table>
        </div>
        <div style="margin-top: 10px;">
          <button class="btn btn-secondary btn-sm" onclick="addNewPersonFromModal()">+ Add Another Person</button>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn btn-primary" onclick="closeBulkEditModal()">Done / Apply Changes</button>
      </div>
    </div>
  </div>

  <!-- ================= MODAL: A4 PRINT PREVIEW ================= -->
  <div class="modal-backdrop no-print" id="printPreviewModal">
    <div class="modal-container" style="width: 950px;">
      <div class="modal-header">
        <div class="modal-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
          <span>A4 Print Preview (Exact 8.0 × 4.5 cm Cards)</span>
        </div>
        <button class="btn btn-dark btn-icon" onclick="closePrintModal()">×</button>
      </div>
      <div style="padding: 8px 16px; background: #f8fafc; border-bottom: 1px solid var(--border); display: flex; align-items: center; justify-content: space-between; font-size: 12px;">
        <div style="display: flex; gap: 12px; align-items: center;">
          <span id="printPageCountSummary" style="font-weight: 700; color: #1e293b;">Page 1 of 1</span>
          <span style="color: var(--text-muted);">Paper: Standard A4 Portrait</span>
          <span style="color: var(--text-muted);">Card Size: 80 × 45 mm</span>
        </div>
        <div style="display: flex; gap: 8px;">
          <button class="btn btn-secondary btn-sm" onclick="closePrintModal()">Close</button>
          <button class="btn btn-success" onclick="triggerSystemPrint()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="6 9 6 2 18 2 18 9"/><path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"/><rect x="6" y="14" width="12" height="8"/></svg>
            Print Now / Save as PDF
          </button>
        </div>
      </div>
      <div class="print-preview-container" id="printPreviewPagesContainer">
        <!-- Virtual A4 Pages injected here -->
      </div>
    </div>
  </div>

  <!-- Hidden Container rendered for Native System Print (A4) -->
  <div id="printContainer"></div>

  <!-- SCRIPT LOGIC -->
  <script>
    // Embedded Default Template Backgrounds (100% Offline, Zero external files needed)
    const DEFAULT_FRONT_B64 = "{front_b64}";
    const DEFAULT_BACK_B64 = "{back_b64}";

    // Standard Default Fields
    const DEFAULT_FRONT_FIELDS = [
      {{ id: 'pp_no', label: 'PP No.', visible: true }},
      {{ id: 'name', label: 'Name', visible: true }},
      {{ id: 'designation', label: 'Designation', visible: true }},
      {{ id: 'country', label: 'Country', visible: true }},
      {{ id: 'validity', label: 'Validity', visible: true }}
    ];

    const DEFAULT_BACK_FIELDS = [
      {{ id: 'sl_no', label: 'SL No.', prefix: 'SL No. 43Wg/ 399 / ', x: 55, y: 90, size: 28, bold: true, color: '#000000', valColor: '#001a70', hasDots: true, visible: true }},
      {{ id: 'iafc_no', label: 'IAFC No.', prefix: 'IAFC No. ', x: 540, y: 90, size: 28, bold: true, color: '#000000', valColor: '#001a70', hasDots: true, visible: true }},
      {{ id: 'vim', label: 'VIM', prefix: 'VIM ', x: 55, y: 175, size: 28, bold: true, color: '#000000', valColor: '#001a70', hasDots: true, visible: true }},
      {{ id: 'validity', label: 'Validity:', prefix: 'Validity: ', x: 55, y: 260, size: 28, bold: true, color: '#000000', valColor: '#000000', underlined: true, hasDots: false, visible: true }}
    ];

    // Application State
    const appState = {{
      activePersonIndex: 0,
      activeSide: 'front', // 'front' | 'back'
      editMode: false,
      zoom: 1.0,
      dragTarget: null,
      selectedItem: null, // For floating in-place editor
      
      settings: {{
        cardWidthMm: 80,
        cardHeightMm: 45,
        printGapMm: 4,
        printRowGapMm: 5,
        cutGuide: 'dashed', // 'dashed', 'solid', 'none'
        printMode: 'both', // 'both', 'front-only', 'back-only'
        cardsPerPage: 5
      }},

      layout: {{
        front: {{
          logoFade: 82, // 82% faded watermark overlay by default
          // Standard Passport Size Placeholder (270 x 350)
          photoBox: {{ x: 105, y: 295, w: 270, h: 350, visible: true, fit: 'contain' }},
          textConfig: {{
            startX: 475,
            startY: 310,
            rowGap: 75,
            labelWidth: 195,
            fontSize: 28,
            fontFamily: 'Arial, sans-serif',
            bold: true,
            labelColor: '#000000',
            valueColor: '#001a70',
            dotStyle: 'clean' // Default clean colon! (Cleaned the dots)
          }},
          // Default front fields (PP No, Name, Designation, Country, Validity)
          fields: JSON.parse(JSON.stringify(DEFAULT_FRONT_FIELDS))
        }},
        back: {{
          defaultFontSize: 26,
          defaultColor: '#001a70',
          photoBox: {{ x: 670, y: 350, w: 250, h: 75, visible: false, fit: 'contain' }},
          // Back Top & Middle Fields
          fields: JSON.parse(JSON.stringify(DEFAULT_BACK_FIELDS)),
          // Signature Line Details
          signatureConfig: {{
            dateLabel: 'Date.',
            dateX: 65,
            dateY: 425,
            dateSize: 24,
            dateColor: '#000000',
            dateBold: true,
            
            authorityLabel: 'Sign of Issuing Authority',
            authorityX: 650,
            authorityY: 425,
            authoritySize: 24,
            authorityColor: '#000000',
            authorityBold: true
          }},
          // Numbered Terms (Editable Paragraphs)
          termsConfig: {{
            x: 65,
            startY: 495,
            rowGap: 42,
            size: 19,
            bold: false,
            color: '#000000',
            items: [
              '1. Property of Govt of India.',
              '2. Not transferable.',
              '3. Loss is to be reported to issuing authority immediately.',
              '4. Finder has no right to retain it and it is to be returned to the nearest Defense installation / Police station.'
            ]
          }}
        }}
      }},

      bg: {{
        front: null,
        back: null,
        frontData: DEFAULT_FRONT_B64,
        backData: DEFAULT_BACK_B64
      }},

      authoritySign: null,

      // Initial People list with clean default samples
      people: [
        {{
          id: 1,
          frontPhoto: null,
          photoOffsetX: 0,
          photoOffsetY: 0,
          photoZoom: 1.0,
          frontValues: {{
            pp_no: '859342-K',
            name: 'SUBHASH CHANDRA',
            designation: 'JWO',
            country: 'INDIA',
            validity: 'TILL POSTED OUT'
          }},
          backValues: {{
            sl_no: '0099',
            iafc_no: 'AFIC NO.',
            vim: 'M-1294',
            validity: 'TILL POSTED OUT',
            date: '15/08/2024'
          }}
        }},
        {{
          id: 2,
          frontPhoto: null,
          photoOffsetX: 0,
          photoOffsetY: 0,
          photoZoom: 1.0,
          frontValues: {{
            pp_no: '912450-H',
            name: 'AMIT SHARMA',
            designation: 'CPL',
            country: 'INDIA',
            validity: 'TILL POSTED OUT'
          }},
          backValues: {{
            sl_no: '0100',
            iafc_no: '912450-H',
            vim: 'A SCAR ON FOREHEAD',
            validity: 'TILL POSTED OUT',
            date: '21/11/2026'
          }}
        }},
        {{
          id: 3,
          frontPhoto: null,
          photoOffsetX: 0,
          photoOffsetY: 0,
          photoZoom: 1.0,
          frontValues: {{
            pp_no: '',
            name: '',
            designation: '',
            country: 'INDIA',
            validity: 'TILL POSTED OUT'
          }},
          backValues: {{
            sl_no: '',
            iafc_no: '',
            vim: '',
            validity: 'TILL POSTED OUT',
            date: '21/11/2026'
          }}
        }}
      ]
    }};

    const canvas = document.getElementById('cardCanvas');
    const ctx = canvas.getContext('2d');

    // Initialize Background Images
    function initBackgrounds(callback) {{
      let loaded = 0;
      function checkDone() {{
        loaded++;
        if (loaded >= 2 && callback) callback();
      }}
      
      const imgFront = new Image();
      imgFront.onload = () => {{ appState.bg.front = imgFront; checkDone(); }};
      imgFront.src = appState.bg.frontData;

      const imgBack = new Image();
      imgBack.onload = () => {{ appState.bg.back = imgBack; checkDone(); }};
      imgBack.src = appState.bg.backData;
    }}

    // Switch active card side
    function switchSide(side) {{
      appState.activeSide = side;
      document.getElementById('btnSideFront').classList.toggle('active', side === 'front');
      document.getElementById('btnSideBack').classList.toggle('active', side === 'back');

      // Sync side toggles in sidebar
      const frontSec = document.getElementById('frontSideDataSection');
      const backSec = document.getElementById('backSideDataSection');
      const btnTogF = document.getElementById('btnSideToggleFront');
      const btnTogB = document.getElementById('btnSideToggleBack');

      if (side === 'front') {{
        frontSec.style.display = 'flex';
        backSec.style.display = 'none';
        btnTogF.style.background = '#0f172a'; btnTogF.style.color = '#fff';
        btnTogB.style.background = 'transparent'; btnTogB.style.color = '#475569';
      }} else {{
        frontSec.style.display = 'none';
        backSec.style.display = 'flex';
        btnTogB.style.background = '#0f172a'; btnTogB.style.color = '#fff';
        btnTogF.style.background = 'transparent'; btnTogF.style.color = '#475569';
      }}

      const bgImg = appState.bg[side];
      if (bgImg) {{
        canvas.width = bgImg.naturalWidth;
        canvas.height = bgImg.naturalHeight;
      }}
      closeFloatingToolbar();
      updateHeaderTitle();
      syncPhotoZoomUI();
      renderFieldsUI();
      renderCanvas();
    }}

    function updateHeaderTitle() {{
      const p = appState.people[appState.activePersonIndex];
      const pName = (p && p.frontValues.name) ? p.frontValues.name : `Person ${{appState.activePersonIndex + 1}} (Blank)`;
      document.getElementById('currentCardTitle').textContent = `Viewing: ${{pName}} (${{appState.activeSide.toUpperCase()}})`;
    }}

    // Switch sidebar tab
    function switchSidebarTab(tab) {{
      document.getElementById('tabDetails').style.display = tab === 'details' ? 'flex' : 'none';
      document.getElementById('tabLayout').style.display = tab === 'layout' ? 'flex' : 'none';
      document.getElementById('printTabContent').style.display = tab === 'print' ? 'flex' : 'none';

      document.getElementById('tabBtnDetails').classList.toggle('active', tab === 'details');
      document.getElementById('tabBtnLayout').classList.toggle('active', tab === 'layout');
      document.getElementById('tabBtnPrint').classList.toggle('active', tab === 'print');
    }}

    // Update Person Select UI
    function renderPersonSelect() {{
      const sel = document.getElementById('personSelect');
      sel.innerHTML = '';
      appState.people.forEach((p, idx) => {{
        const opt = document.createElement('option');
        opt.value = idx;
        const name = p.frontValues.name ? p.frontValues.name : `Person ${{idx + 1}} (Blank)`;
        const desig = p.frontValues.designation ? ` (${{p.frontValues.designation}})` : '';
        opt.textContent = `${{idx + 1}}. ${{name}}${{desig}}`;
        if (idx === appState.activePersonIndex) opt.selected = true;
        sel.appendChild(opt);
      }});

      document.getElementById('peopleCountBadge').textContent = `${{appState.people.length}} Person${{appState.people.length > 1 ? 's' : ''}}`;
      updateHeaderTitle();
      syncPhotoZoomUI();
    }}

    function selectPerson(idx) {{
      appState.activePersonIndex = Math.max(0, Math.min(idx, appState.people.length - 1));
      renderPersonSelect();
      renderFieldsUI();
      renderCanvas();
    }}

    function navigatePerson(direction) {{
      const newIdx = appState.activePersonIndex + direction;
      if (newIdx >= 0 && newIdx < appState.people.length) {{
        selectPerson(newIdx);
      }}
    }}

    function addNewPerson() {{
      const newId = Date.now();
      const newPerson = {{
        id: newId,
        frontPhoto: null,
        photoOffsetX: 0,
        photoOffsetY: 0,
        photoZoom: 1.0,
        frontValues: {{}},
        backValues: {{}}
      }};
      // initialize empty values
      appState.layout.front.fields.forEach(f => {{
        if (f.id === 'country') newPerson.frontValues[f.id] = 'INDIA';
        else if (f.id === 'validity') newPerson.frontValues[f.id] = 'TILL POSTED OUT';
        else newPerson.frontValues[f.id] = '';
      }});
      appState.layout.back.fields.forEach(f => {{
        const prev = appState.people[appState.people.length - 1];
        if (prev && (f.id === 'validity' || f.id === 'date')) {{
          newPerson.backValues[f.id] = prev.backValues[f.id] || 'TILL POSTED OUT';
        }} else {{
          newPerson.backValues[f.id] = '';
        }}
      }});
      newPerson.backValues.date = (appState.people[0] && appState.people[0].backValues.date) || '21/11/2026';
      newPerson.backValues.validity = 'TILL POSTED OUT';

      appState.people.push(newPerson);
      selectPerson(appState.people.length - 1);
      saveToStorage();
    }}

    function duplicateCurrentPerson() {{
      const current = appState.people[appState.activePersonIndex];
      if (!current) return;
      const copy = JSON.parse(JSON.stringify(current));
      copy.id = Date.now();
      if (current.frontPhoto) copy.frontPhoto = current.frontPhoto;
      appState.people.splice(appState.activePersonIndex + 1, 0, copy);
      selectPerson(appState.activePersonIndex + 1);
      saveToStorage();
    }}

    function deleteCurrentPerson() {{
      if (appState.people.length <= 1) {{
        alert('At least one person is required.');
        return;
      }}
      if (confirm(`Delete Person ${{appState.activePersonIndex + 1}}?`)) {{
        appState.people.splice(appState.activePersonIndex, 1);
        appState.activePersonIndex = Math.max(0, appState.activePersonIndex - 1);
        selectPerson(appState.activePersonIndex);
        saveToStorage();
      }}
    }}

    // Render Fields in Sidebar: Large comfortable cards with full-width value inputs!
    function renderFieldsUI() {{
      const current = appState.people[appState.activePersonIndex];
      if (!current) return;

      // Front fields container
      const frontContainer = document.getElementById('frontFieldsList');
      frontContainer.innerHTML = '';
      appState.layout.front.fields.forEach((f, idx) => {{
        const val = current.frontValues[f.id] || '';
        const isVis = (f.visible !== false);
        const card = document.createElement('div');
        card.className = 'field-entry-card';
        if (!isVis) {{
          card.style.opacity = '0.65';
          card.style.borderStyle = 'dashed';
          card.style.background = '#f8fafc';
        }}
        card.innerHTML = `
          <div class="field-entry-header">
            <div class="field-label-wrapper">
              <span class="field-tag-badge" style="background:${{isVis ? '#dbeafe' : '#f1f5f9'}}; color:${{isVis ? '#1e40af' : '#64748b'}};">${{isVis ? 'FRONT' : 'HIDDEN'}}</span>
              <input type="text" class="field-name-text" value="${{escapeHtml(f.label)}}" title="Click to rename field" onchange="updateFieldLabelDirect('front', '${{f.id}}', this.value)" />
            </div>
            <div style="display: flex; gap: 4px; align-items: center;">
              <button class="btn btn-xs ${{isVis ? 'btn-secondary' : 'btn-dark'}}" 
                      style="display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; font-size: 11px; font-weight: 600; ${{isVis ? 'background: #f1f5f9; color: #334155;' : 'background: #fee2e2; color: #dc2626; border-color: #fca5a5;'}}" 
                      title="${{isVis ? 'Click to hide this field on the card' : 'Click to show this field on the card'}}" 
                      onclick="toggleFieldVisibility('front', '${{f.id}}')">
                ${{isVis 
                  ? `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg> Visible` 
                  : `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg> Hidden`}}
              </button>
            </div>
          </div>
          <input type="text" class="field-value-input-large" value="${{escapeHtml(val)}}" placeholder="${{isVis ? 'Type ' + escapeHtml(f.label) + ' value...' : '(Field is Hidden on card) Type value...'}}" oninput="updatePersonValue('front', '${{f.id}}', this.value)" />
        `;
        frontContainer.appendChild(card);
      }});

      // Back fields container
      const backContainer = document.getElementById('backFieldsList');
      backContainer.innerHTML = '';
      appState.layout.back.fields.forEach((f, idx) => {{
        const val = current.backValues[f.id] || '';
        const isVis = (f.visible !== false);
        const card = document.createElement('div');
        card.className = 'field-entry-card';
        if (!isVis) {{
          card.style.opacity = '0.65';
          card.style.borderStyle = 'dashed';
          card.style.background = '#f8fafc';
        }}
        card.innerHTML = `
          <div class="field-entry-header">
            <div class="field-label-wrapper">
              <span class="field-tag-badge" style="background:${{isVis ? '#e0f2fe' : '#f1f5f9'}}; color:${{isVis ? '#0369a1' : '#64748b'}};">${{isVis ? 'BACK' : 'HIDDEN'}}</span>
              <input type="text" class="field-name-text" value="${{escapeHtml(f.prefix || f.label)}}" title="Click to edit prefix" onchange="updateFieldPrefixDirect('${{f.id}}', this.value)" />
            </div>
            <div style="display: flex; gap: 4px; align-items: center;">
              <button class="btn btn-xs ${{isVis ? 'btn-secondary' : 'btn-dark'}}" 
                      style="display: inline-flex; align-items: center; gap: 4px; padding: 3px 8px; font-size: 11px; font-weight: 600; ${{isVis ? 'background: #f1f5f9; color: #334155;' : 'background: #fee2e2; color: #dc2626; border-color: #fca5a5;'}}" 
                      title="${{isVis ? 'Click to hide this field on the card' : 'Click to show this field on the card'}}" 
                      onclick="toggleFieldVisibility('back', '${{f.id}}')">
                ${{isVis 
                  ? `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg> Visible` 
                  : `<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg> Hidden`}}
              </button>
            </div>
          </div>
          <input type="text" class="field-value-input-large" value="${{escapeHtml(val)}}" placeholder="${{isVis ? 'Enter ' + escapeHtml(f.label) + ' value...' : '(Field is Hidden on card) Enter value...'}}" oninput="updatePersonValue('back', '${{f.id}}', this.value)" />
        `;
        backContainer.appendChild(card);
      }});

      // Back Date input sync
      const dateInp = document.getElementById('backDateInput');
      if (dateInp) dateInp.value = current.backValues.date || '21/11/2026';

      // Back Terms list sync
      const termsContainer = document.getElementById('backTermsList');
      if (termsContainer) {{
        termsContainer.innerHTML = '';
        appState.layout.back.termsConfig.items.forEach((termText, tIdx) => {{
          const tRow = document.createElement('div');
          tRow.style.display = 'flex';
          tRow.style.gap = '6px';
          tRow.innerHTML = `
            <input type="text" class="form-input" style="padding:6px 8px; font-size:12px; border:1px solid #cbd5e1; border-radius:6px; flex:1;" value="${{escapeHtml(termText)}}" oninput="updateTermText(${{tIdx}}, this.value)" />
          `;
          termsContainer.appendChild(tRow);
        }});
      }}

      // Sync Layout Controls Inputs
      syncLayoutControls();
      syncPhotoZoomUI();
    }}

    function updateFieldLabelDirect(side, fieldId, newLabel) {{
      const fieldList = side === 'front' ? appState.layout.front.fields : appState.layout.back.fields;
      const f = fieldList.find(x => x.id === fieldId);
      if (f && newLabel.trim()) {{
        f.label = newLabel.trim();
        renderCanvas();
        saveToStorage();
      }}
    }}

    function updateFieldPrefixDirect(fieldId, newPrefix) {{
      const f = appState.layout.back.fields.find(x => x.id === fieldId);
      if (f) {{
        f.prefix = newPrefix;
        f.label = newPrefix;
        renderCanvas();
        saveToStorage();
      }}
    }}

    function updatePersonValue(side, fieldId, value) {{
      const current = appState.people[appState.activePersonIndex];
      if (!current) return;
      if (side === 'front') {{
        current.frontValues[fieldId] = value;
      }} else {{
        current.backValues[fieldId] = value;
      }}
      if (fieldId === 'name' || fieldId === 'designation') {{
        renderPersonSelect();
      }}
      renderCanvas();
      debouncedSave();
    }}

    function updateBackDate(value) {{
      const current = appState.people[appState.activePersonIndex];
      if (current) {{
        current.backValues.date = value;
        renderCanvas();
        debouncedSave();
      }}
    }}

    function updateTermText(idx, text) {{
      appState.layout.back.termsConfig.items[idx] = text;
      renderCanvas();
      debouncedSave();
    }}

    function addNewField(side) {{
      const label = prompt('Enter name of new field (e.g., Blood Group, Branch, Ser No):');
      if (!label || !label.trim()) return;
      const cleanLabel = label.trim();
      const id = 'field_' + Date.now();
      
      if (side === 'front') {{
        appState.layout.front.fields.push({{ id, label: cleanLabel, visible: true }});
      }} else {{
        appState.layout.back.fields.push({{
          id, label: cleanLabel, prefix: cleanLabel + ' : ', x: 55, y: 340, size: 28, bold: true, color: '#000000', valColor: '#001a70', hasDots: true, visible: true
        }});
      }}
      
      // initialize field in all people
      appState.people.forEach(p => {{
        if (side === 'front') p.frontValues[id] = '';
        else p.backValues[id] = '';
      }});

      renderFieldsUI();
      renderCanvas();
      saveToStorage();
    }}

    function toggleFieldVisibility(side, fieldId) {{
      const fieldList = (side === 'front') ? appState.layout.front.fields : appState.layout.back.fields;
      const f = fieldList.find(x => x.id === fieldId);
      if (f) {{
        f.visible = (f.visible === false) ? true : false;
        renderFieldsUI();
        renderCanvas();
        debouncedSave();
      }}
    }}

    function resetDefaultFields(side) {{
      if (confirm(`Reset ${{side}} side fields back to standard defaults?`)) {{
        if (side === 'front') {{
          appState.layout.front.fields = JSON.parse(JSON.stringify(DEFAULT_FRONT_FIELDS));
        }} else {{
          appState.layout.back.fields = JSON.parse(JSON.stringify(DEFAULT_BACK_FIELDS));
        }}
        renderFieldsUI();
        renderCanvas();
        saveToStorage();
      }}
    }}

    function removeField(side, fieldId) {{
      const fieldList = side === 'front' ? appState.layout.front.fields : appState.layout.back.fields;
      const f = fieldList.find(x => x.id === fieldId);
      if (!f) return;
      if (confirm(`Remove "${{f.label}}" and its values from all cards?`)) {{
        if (side === 'front') {{
          appState.layout.front.fields = appState.layout.front.fields.filter(x => x.id !== fieldId);
          appState.people.forEach(p => {{ delete p.frontValues[fieldId]; }});
        }} else {{
          appState.layout.back.fields = appState.layout.back.fields.filter(x => x.id !== fieldId);
          appState.people.forEach(p => {{ delete p.backValues[fieldId]; }});
        }}
        renderFieldsUI();
        renderCanvas();
        saveToStorage();
      }}
    }}

    function applyCommonBackValuesToAll() {{
      const current = appState.people[appState.activePersonIndex];
      if (!current) return;
      const valValidity = current.backValues.validity || 'TILL POSTED OUT';
      const valDate = current.backValues.date || '21/11/2026';
      if (!confirm(`Apply Validity ("${{valValidity}}") and Date ("${{valDate}}") to all ${{appState.people.length}} people?`)) return;

      appState.people.forEach(p => {{
        p.backValues.validity = valValidity;
        p.backValues.date = valDate;
      }});
      alert('Applied to all people.');
      saveToStorage();
    }}

    // ================= PHOTOS & DRAG TO PAN =================
    function uploadPersonPhoto(e) {{
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (event) => {{
        const img = new Image();
        img.onload = () => {{
          const current = appState.people[appState.activePersonIndex];
          if (current) {{
            current.frontPhoto = img;
            current.frontPhotoData = event.target.result;
            current.photoOffsetX = 0;
            current.photoOffsetY = 0;
            current.photoZoom = 1.0;
            syncPhotoZoomUI();
            renderCanvas();
            saveToStorage();
          }}
        }};
        img.src = event.target.result;
      }};
      reader.readAsDataURL(file);
      e.target.value = '';
    }}

    function clearCurrentPhoto() {{
      const current = appState.people[appState.activePersonIndex];
      if (current) {{
        current.frontPhoto = null;
        current.frontPhotoData = null;
        current.photoOffsetX = 0;
        current.photoOffsetY = 0;
        current.photoZoom = 1.0;
        syncPhotoZoomUI();
        renderCanvas();
        saveToStorage();
      }}
    }}

    function setPhotoZoom(val) {{
      const current = appState.people[appState.activePersonIndex];
      if (current) {{
        current.photoZoom = Math.max(0.5, Math.min(3.0, val));
        syncPhotoZoomUI();
        renderCanvas();
        debouncedSave();
      }}
    }}

    function adjustPhotoZoom(delta) {{
      const current = appState.people[appState.activePersonIndex];
      if (current) {{
        const curZoom = current.photoZoom || 1.0;
        setPhotoZoom(Math.round((curZoom + delta) * 100) / 100);
      }}
    }}

    function resetPhotoPosition() {{
      const current = appState.people[appState.activePersonIndex];
      if (current) {{
        current.photoOffsetX = 0;
        current.photoOffsetY = 0;
        current.photoZoom = 1.0;
        syncPhotoZoomUI();
        renderCanvas();
        saveToStorage();
      }}
    }}

    function syncPhotoZoomUI() {{
      const current = appState.people[appState.activePersonIndex];
      const zoom = (current && current.photoZoom) ? current.photoZoom : 1.0;
      const slider = document.getElementById('photoZoomSlider');
      if (slider) slider.value = zoom;
      const text = document.getElementById('photoZoomText');
      if (text) text.textContent = `${{Math.round(zoom * 100)}}%`;
    }}

    function uploadAuthoritySign(e) {{
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (event) => {{
        const img = new Image();
        img.onload = () => {{
          appState.authoritySign = img;
          appState.authoritySignData = event.target.result;
          renderCanvas();
          saveToStorage();
        }};
        img.src = event.target.result;
      }};
      reader.readAsDataURL(file);
      e.target.value = '';
    }}

    function clearAuthoritySign() {{
      appState.authoritySign = null;
      appState.authoritySignData = null;
      renderCanvas();
      saveToStorage();
    }}

    // ================= LAYOUT CONTROLS =================
    function syncLayoutControls() {{
      const cfg = appState.layout.front.textConfig;
      document.getElementById('dotStyleSelect').value = cfg.dotStyle || 'clean';
      document.getElementById('cfgStartX').value = cfg.startX;
      document.getElementById('cfgStartY').value = cfg.startY;
      document.getElementById('cfgRowGap').value = cfg.rowGap;
      document.getElementById('cfgLabelWidth').value = cfg.labelWidth;
      document.getElementById('cfgFontSize').value = cfg.fontSize;
      document.getElementById('cfgValueColor').value = cfg.valueColor;
      document.getElementById('cfgBold').checked = cfg.bold;

      // Photo box controls
      const pb = appState.layout.front.photoBox;
      document.getElementById('cfgPhotoW').value = pb.w;
      document.getElementById('cfgPhotoH').value = pb.h;

      // Logo fade slider
      const fade = appState.layout.front.logoFade ?? 82;
      document.getElementById('cfgLogoFade').value = fade;
      document.getElementById('logoFadeValueText').textContent = `${{fade}}% Faded`;
    }}

    function updateLogoFade(val) {{
      appState.layout.front.logoFade = val;
      document.getElementById('logoFadeValueText').textContent = `${{val}}% Faded`;
      renderCanvas();
      debouncedSave();
    }}

    function updateTextConfig(key, value) {{
      appState.layout.front.textConfig[key] = value;
      renderCanvas();
      saveToStorage();
    }}

    function updatePhotoBox(key, value) {{
      appState.layout.front.photoBox[key] = value;
      renderCanvas();
      saveToStorage();
    }}

    function resetPhotoBoxToStandard() {{
      appState.layout.front.photoBox = {{ x: 105, y: 295, w: 270, h: 350, visible: true, fit: 'contain' }};
      syncLayoutControls();
      renderCanvas();
      saveToStorage();
    }}

    function toggleLayoutMode(enabled) {{
      appState.editMode = enabled;
      document.body.classList.toggle('layout-unlocked', enabled);
      const banner = document.getElementById('editBanner');
      banner.classList.toggle('unlocked', enabled);
      document.getElementById('lockStatusBadge').textContent = enabled ? 'UNLOCKED' : 'LOCKED';
      document.getElementById('lockStatusBadge').className = enabled ? 'badge blue' : 'badge';
      document.getElementById('stageHint').textContent = enabled
        ? 'Layout Unlocked: Drag text fields directly on card. Click text to edit with floating toolbar.'
        : '💡 Click any text on the card to edit with the modern floating toolbar. Drag photo to center face.';
      renderCanvas();
    }}

    // Custom Background Uploads
    function changeCustomBg(e, side) {{
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (event) => {{
        const img = new Image();
        img.onload = () => {{
          appState.bg[side] = img;
          appState.bg[side + 'Data'] = event.target.result;
          if (appState.activeSide === side) {{
            canvas.width = img.naturalWidth;
            canvas.height = img.naturalHeight;
          }}
          renderCanvas();
          saveToStorage();
        }};
        img.src = event.target.result;
      }};
      reader.readAsDataURL(file);
      e.target.value = '';
    }}

    function resetDefaultBackgrounds() {{
      appState.bg.frontData = DEFAULT_FRONT_B64;
      appState.bg.backData = DEFAULT_BACK_B64;
      initBackgrounds(() => {{
        switchSide(appState.activeSide);
        saveToStorage();
      }});
    }}

    // Zoom Controls
    function adjustZoom(delta) {{
      appState.zoom = Math.max(0.3, Math.min(2.5, appState.zoom + delta));
      applyZoom();
    }}

    function resetZoom() {{
      const vp = document.getElementById('canvasViewport');
      if (vp) {{
        const availW = vp.clientWidth - 48;
        const availH = vp.clientHeight - 48;
        const scale = Math.min(availW / canvas.width, availH / canvas.height, 1.0);
        appState.zoom = Math.round(scale * 10) / 10 || 1.0;
      }} else {{
        appState.zoom = 1.0;
      }}
      applyZoom();
    }}

    function applyZoom() {{
      canvas.style.transform = `scale(${{appState.zoom}})`;
      canvas.style.transformOrigin = 'center center';
      document.getElementById('zoomLevelText').textContent = `${{Math.round(appState.zoom * 100)}}%`;
    }}

    // Helper: Escape HTML
    function escapeHtml(str) {{
      return String(str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
    }}

    // ================= CARD RENDERING ENGINE =================
    // Draw photo strictly contained inside standard box with user's pan and zoom
    function drawContainedPhoto(targetCtx, img, pb, person) {{
      targetCtx.save();

      // 1. Strictly clip to box boundaries (ZERO overflow outside the box!)
      targetCtx.beginPath();
      targetCtx.rect(pb.x, pb.y, pb.w, pb.h);
      targetCtx.clip();

      // 2. Clear background inside photo frame to clean white
      targetCtx.fillStyle = '#ffffff';
      targetCtx.fillRect(pb.x, pb.y, pb.w, pb.h);

      // 3. Compute auto-contain base dimensions
      const imgRatio = img.naturalWidth / img.naturalHeight;
      const boxRatio = pb.w / pb.h;
      let baseW, baseH;
      if (imgRatio > boxRatio) {{
        baseW = pb.w;
        baseH = pb.w / imgRatio;
      }} else {{
        baseH = pb.h;
        baseW = pb.h * imgRatio;
      }}

      // 4. User zoom multiplier (default 1.0)
      const zoom = (person && person.photoZoom) ? person.photoZoom : 1.0;
      const drawW = baseW * zoom;
      const drawH = baseH * zoom;

      // 5. User pan offsets (drag inside box)
      const offX = (person && person.photoOffsetX) ? person.photoOffsetX : 0;
      const offY = (person && person.photoOffsetY) ? person.photoOffsetY : 0;
      const drawX = pb.x + (pb.w - drawW) / 2 + offX;
      const drawY = pb.y + (pb.h - drawH) / 2 + offY;

      // 6. Draw image
      targetCtx.drawImage(img, drawX, drawY, drawW, drawH);

      targetCtx.restore();
    }}

    // Registry of rendered text bounds for click-to-edit and floating toolbar
    let renderedElements = [];

    // Universal Card Drawer
    function drawCard(targetCtx, side, person, forExport = false) {{
      const w = targetCtx.canvas.width;
      const h = targetCtx.canvas.height;
      targetCtx.clearRect(0, 0, w, h);
      if (!forExport) {{
        renderedElements = [];
        window.__renderedElements = renderedElements;
      }}

      // 1. Draw Background Template
      const bgImg = appState.bg[side];
      if (bgImg) {{
        targetCtx.drawImage(bgImg, 0, 0, w, h);
      }} else {{
        targetCtx.fillStyle = '#ffffff';
        targetCtx.fillRect(0, 0, w, h);
      }}

      // 2. Draw Front Side Elements
      if (side === 'front') {{
        
        // A. Fade the Middle Logo / Watermark
        const fadePercent = appState.layout.front.logoFade ?? 82;
        if (fadePercent > 0) {{
          targetCtx.save();
          targetCtx.fillStyle = `rgba(255, 255, 255, ${{fadePercent / 100}})`;
          targetCtx.fillRect(375, 245, 275, 480);
          targetCtx.restore();
        }}

        // B. Standard Profile Photo Box
        const pb = appState.layout.front.photoBox;
        if (pb && pb.visible) {{
          targetCtx.save();
          targetCtx.fillStyle = '#ffffff';
          targetCtx.fillRect(pb.x, pb.y, pb.w, pb.h);
          targetCtx.restore();

          if (person && person.frontPhoto) {{
            drawContainedPhoto(targetCtx, person.frontPhoto, pb, person);
          }} else {{
            // Clean standard photo frame placeholder
            targetCtx.save();
            targetCtx.fillStyle = '#f8fafc';
            targetCtx.fillRect(pb.x, pb.y, pb.w, pb.h);
            targetCtx.strokeStyle = '#64748b';
            targetCtx.lineWidth = 1.5;
            targetCtx.strokeRect(pb.x, pb.y, pb.w, pb.h);
            targetCtx.fillStyle = '#94a3b8';
            targetCtx.font = 'bold 18px Arial, sans-serif';
            targetCtx.textAlign = 'center';
            targetCtx.textBaseline = 'middle';
            targetCtx.fillText('PASSPORT PHOTO', pb.x + pb.w / 2, pb.y + pb.h / 2);
            targetCtx.restore();
          }}

          // Frame outline
          targetCtx.strokeStyle = '#0f172a';
          targetCtx.lineWidth = 2;
          targetCtx.strokeRect(pb.x, pb.y, pb.w, pb.h);
        }}

        // C. Front Text Fields (Clean Colon by Default!)
        const cfg = appState.layout.front.textConfig;
        const fields = appState.layout.front.fields;
        const fontName = cfg.fontFamily || 'Arial, sans-serif';
        const fontSize = cfg.fontSize || 28;
        const fontBold = cfg.bold ? 'bold ' : '';
        const endRowX = w - 40;

        // Only render visible fields
        const visibleFrontFields = fields.filter(f => f.visible !== false);

        visibleFrontFields.forEach((f, idx) => {{
          const rowY = cfg.startY + (idx * cfg.rowGap);
          const rowX = cfg.startX;
          const val = (person && person.frontValues[f.id]) ? String(person.frontValues[f.id]).trim() : '';

          targetCtx.textBaseline = 'top';
          targetCtx.font = `${{fontBold}}${{fontSize}}px ${{fontName}}`;

          // Label
          targetCtx.fillStyle = cfg.labelColor || '#000000';
          const labelText = f.label || '';
          targetCtx.fillText(labelText, rowX, rowY);
          const measuredLabelWidth = targetCtx.measureText(labelText).width;

          // Colon and value positions
          const colonX = Math.max(rowX + cfg.labelWidth - 14, rowX + measuredLabelWidth + 8);
          const valStartX = colonX + 16;
          const singleDotWidth = targetCtx.measureText('. ').width;

          // Dot Style Rendering (DEFAULT: CLEAN COLON, NO DOTS)
          const dotStyle = cfg.dotStyle || 'clean';

          if (dotStyle === 'clean') {{
            targetCtx.fillStyle = cfg.labelColor || '#000000';
            targetCtx.fillText(':', colonX, rowY);
            if (val) {{
              targetCtx.fillStyle = cfg.valueColor || '#001a70';
              targetCtx.fillText(val, valStartX, rowY);
            }}
          }} else if (dotStyle === 'colon-dots') {{
            targetCtx.fillStyle = cfg.labelColor || '#000000';
            targetCtx.fillText(':', colonX, rowY);
            if (val) {{
              targetCtx.fillStyle = cfg.valueColor || '#001a70';
              targetCtx.fillText(val, valStartX, rowY);
              const valWidth = targetCtx.measureText(val).width;
              const trailStartX = valStartX + valWidth + 10;
              const trailWidth = Math.max(0, endRowX - trailStartX);
              const trailDots = Math.floor(trailWidth / singleDotWidth);
              if (trailDots > 0) {{
                targetCtx.fillStyle = '#64748b';
                targetCtx.fillText('. '.repeat(trailDots), trailStartX, rowY);
              }}
            }} else {{
              const trailWidth = Math.max(0, endRowX - valStartX);
              const fullDots = Math.floor(trailWidth / singleDotWidth);
              if (fullDots > 0) {{
                targetCtx.fillStyle = '#64748b';
                targetCtx.fillText('. '.repeat(fullDots), valStartX, rowY);
              }}
            }}
          }} else if (dotStyle === 'dots-nearby') {{
            targetCtx.fillStyle = '#64748b';
            targetCtx.fillText('. .', colonX - 4, rowY);
            if (val) {{
              targetCtx.fillStyle = cfg.valueColor || '#001a70';
              targetCtx.fillText(val, valStartX, rowY);
              const valWidth = targetCtx.measureText(val).width;
              const trailStartX = valStartX + valWidth + 10;
              const trailWidth = Math.max(0, endRowX - trailStartX);
              const trailDots = Math.floor(trailWidth / singleDotWidth);
              if (trailDots > 0) {{
                targetCtx.fillStyle = '#64748b';
                targetCtx.fillText('. '.repeat(trailDots), trailStartX, rowY);
              }}
            }}
          }} else if (dotStyle === 'leader') {{
            const dotStartX = colonX + 6;
            const fullSpanWidth = Math.max(0, endRowX - dotStartX);
            if (val) {{
              const valWidth = targetCtx.measureText(val).width;
              const leaderWidth = Math.max(0, fullSpanWidth - valWidth - 10);
              const leaderDotCount = Math.floor(leaderWidth / singleDotWidth);
              if (leaderDotCount > 0) {{
                targetCtx.fillStyle = '#64748b';
                targetCtx.fillText('. '.repeat(leaderDotCount), dotStartX, rowY);
              }}
              targetCtx.fillStyle = cfg.valueColor || '#001a70';
              targetCtx.fillText(val, dotStartX + leaderWidth + 6, rowY);
            }} else {{
              const fullDots = Math.floor(fullSpanWidth / singleDotWidth);
              if (fullDots > 0) {{
                targetCtx.fillStyle = '#64748b';
                targetCtx.fillText('. '.repeat(fullDots), dotStartX, rowY);
              }}
            }}
          }} else if (dotStyle === 'value-on-dots') {{
            const dotStartX = colonX + 6;
            const fullSpanWidth = Math.max(0, endRowX - dotStartX);
            const fullDots = Math.floor(fullSpanWidth / singleDotWidth);
            if (fullDots > 0) {{
              targetCtx.fillStyle = '#94a3b8';
              targetCtx.fillText('. '.repeat(fullDots), dotStartX, rowY);
            }}
            if (val) {{
              targetCtx.fillStyle = cfg.valueColor || '#001a70';
              targetCtx.fillText(val, valStartX, rowY);
            }}
          }}

          // Track element for floating editor
          if (!forExport) {{
            const totalW = Math.max(260, measuredLabelWidth + 30 + targetCtx.measureText(val || '     ').width);
            renderedElements.push({{
              type: 'front-field',
              id: f.id,
              label: f.label,
              val: val,
              x: rowX,
              y: rowY,
              w: totalW,
              h: fontSize + 6,
              fontSize: fontSize,
              bold: cfg.bold,
              color: cfg.valueColor
            }});
          }}
        }});
      }}

      // 3. Draw Back Side Elements (Complete Native Editable Back Side)
      if (side === 'back') {{
        const bLayout = appState.layout.back;
        const fields = bLayout.fields;

        // Top & Middle Fields
        fields.forEach(f => {{
          if (f.visible === false) return; // Skip hidden back fields
          const val = (person && person.backValues[f.id]) ? String(person.backValues[f.id]).trim() : '';
          const fSize = f.size || bLayout.defaultFontSize || 28;
          targetCtx.font = `${{f.bold ? 'bold ' : ''}}${{fSize}}px Arial, sans-serif`;
          targetCtx.textBaseline = 'top';

          // Label / Prefix
          targetCtx.fillStyle = f.color || '#000000';
          const prefixText = f.prefix || (f.label + ' : ');
          targetCtx.fillText(prefixText, f.x, f.y);
          const prefixW = targetCtx.measureText(prefixText).width;

          // Value and Dotted lines
          const valX = f.x + prefixW + 6;
          const endLimitX = (f.id === 'sl_no') ? 510 : (w - 50);

          if (f.underlined) {{
            // Validity: TILL POSTED OUT (underlined)
            const displayVal = val || 'TILL POSTED OUT';
            targetCtx.fillStyle = f.valColor || '#000000';
            targetCtx.fillText(displayVal, valX, f.y);
            const valW = targetCtx.measureText(displayVal).width;
            targetCtx.lineWidth = 2.5;
            targetCtx.strokeStyle = '#000000';
            targetCtx.beginPath();
            targetCtx.moveTo(valX, f.y + fSize + 4);
            targetCtx.lineTo(valX + valW + 10, f.y + fSize + 4);
            targetCtx.stroke();
          }} else if (f.hasDots) {{
            // Dotted Leader + Value
            const dotW = targetCtx.measureText('. ').width;
            if (val) {{
              targetCtx.fillStyle = f.valColor || '#001a70';
              targetCtx.fillText(val, valX, f.y);
              const valW = targetCtx.measureText(val).width;
              const trailX = valX + valW + 8;
              const trailW = Math.max(0, endLimitX - trailX);
              const dotsCount = Math.floor(trailW / dotW);
              if (dotsCount > 0) {{
                targetCtx.fillStyle = '#64748b';
                targetCtx.fillText('. '.repeat(dotsCount), trailX, f.y);
              }}
            }} else {{
              const trailW = Math.max(0, endLimitX - valX);
              const dotsCount = Math.floor(trailW / dotW);
              if (dotsCount > 0) {{
                targetCtx.fillStyle = '#64748b';
                targetCtx.fillText('. '.repeat(dotsCount), valX, f.y);
              }}
            }}
          }} else {{
            targetCtx.fillStyle = f.valColor || '#001a70';
            targetCtx.fillText(val, valX, f.y);
          }}

          // Track element for floating editor
          if (!forExport) {{
            renderedElements.push({{
              type: 'back-field',
              id: f.id,
              label: f.label,
              val: val,
              x: f.x,
              y: f.y,
              w: Math.max(160, prefixW + targetCtx.measureText(val || '     ').width + 20),
              h: fSize + 6,
              fontSize: fSize,
              bold: f.bold,
              color: f.valColor
            }});
          }}
        }});

        // Signature Line & Date
        const sigCfg = bLayout.signatureConfig;
        const curDate = (person && person.backValues.date) ? person.backValues.date : '21/11/2026';

        // Date.  21/11/2026
        targetCtx.font = `${{sigCfg.dateBold ? 'bold ' : ''}}${{sigCfg.dateSize || 24}}px Arial, sans-serif`;
        targetCtx.fillStyle = sigCfg.dateColor || '#000000';
        targetCtx.textBaseline = 'top';
        const dateString = `${{sigCfg.dateLabel}}  ${{curDate}}`;
        targetCtx.fillText(dateString, sigCfg.dateX, sigCfg.dateY);

        if (!forExport) {{
          renderedElements.push({{
            type: 'back-date',
            id: 'date',
            label: 'Date',
            val: curDate,
            x: sigCfg.dateX,
            y: sigCfg.dateY,
            w: targetCtx.measureText(dateString).width + 10,
            h: (sigCfg.dateSize || 24) + 6,
            fontSize: sigCfg.dateSize || 24,
            bold: sigCfg.dateBold,
            color: sigCfg.dateColor
          }});
        }}

        // Sign of Issuing Authority
        targetCtx.font = `${{sigCfg.authorityBold ? 'bold ' : ''}}${{sigCfg.authoritySize || 24}}px Arial, sans-serif`;
        targetCtx.fillStyle = sigCfg.authorityColor || '#000000';
        targetCtx.fillText(sigCfg.authorityLabel, sigCfg.authorityX, sigCfg.authorityY);

        // Uploaded Authority Signature / Stamp
        if (appState.authoritySign) {{
          targetCtx.drawImage(appState.authoritySign, sigCfg.authorityX + 20, sigCfg.authorityY - 80, 240, 75);
        }}

        // Numbered Terms (Below Horizontal Line)
        const tCfg = bLayout.termsConfig;
        targetCtx.font = `${{tCfg.bold ? 'bold ' : ''}}${{tCfg.size || 22}}px Arial, sans-serif`;
        targetCtx.fillStyle = tCfg.color || '#000000';
        targetCtx.textBaseline = 'top';

        tCfg.items.forEach((termText, tIdx) => {{
          const termY = tCfg.startY + (tIdx * tCfg.rowGap);
          targetCtx.fillText(termText, tCfg.x, termY);

          if (!forExport) {{
            renderedElements.push({{
              type: 'back-term',
              id: tIdx,
              label: `Term ${{tIdx + 1}}`,
              val: termText,
              x: tCfg.x,
              y: termY,
              w: targetCtx.measureText(termText).width + 10,
              h: (tCfg.size || 22) + 6,
              fontSize: tCfg.size || 22,
              bold: tCfg.bold,
              color: tCfg.color
            }});
          }}
        }});
      }}

      // Highlight selected element on canvas if active
      if (!forExport && appState.selectedItem) {{
        targetCtx.save();
        targetCtx.strokeStyle = '#2563eb';
        targetCtx.lineWidth = 2;
        targetCtx.setLineDash([4, 4]);
        targetCtx.strokeRect(appState.selectedItem.x - 4, appState.selectedItem.y - 2, appState.selectedItem.w + 8, appState.selectedItem.h + 4);
        targetCtx.restore();
      }}
    }}

    // Render active canvas
    function renderCanvas() {{
      const person = appState.people[appState.activePersonIndex];
      drawCard(ctx, appState.activeSide, person, false);
    }}

    // ================= MODERN FLOATING INLINE TEXT EDITOR =================
    function getCanvasPos(e) {{
      const rect = canvas.getBoundingClientRect();
      const scaleX = canvas.width / rect.width;
      const scaleY = canvas.height / rect.height;
      return {{
        x: (e.clientX - rect.left) * scaleX,
        y: (e.clientY - rect.top) * scaleY
      }};
    }}

    let isDraggingPhoto = false;
    let dragStartX = 0;
    let dragStartY = 0;

    canvas.addEventListener('mousedown', e => {{
      const pos = getCanvasPos(e);
      const person = appState.people[appState.activePersonIndex];

      // A. DRAG PHOTO INSIDE BOX (Front Side)
      if (appState.activeSide === 'front') {{
        const pb = appState.layout.front.photoBox;
        if (person && person.frontPhoto &&
            pos.x >= pb.x && pos.x <= pb.x + pb.w &&
            pos.y >= pb.y && pos.y <= pb.y + pb.h) {{
          isDraggingPhoto = true;
          dragStartX = pos.x;
          dragStartY = pos.y;
          canvas.style.cursor = 'move';
          closeFloatingToolbar();
          return;
        }}
      }}

      // B. CLICK ON TEXT TO EDIT (Floating Toolbar)
      for (const el of renderedElements) {{
        if (pos.x >= el.x - 6 && pos.x <= el.x + el.w + 6 &&
            pos.y >= el.y - 4 && pos.y <= el.y + el.h + 4) {{
          openFloatingToolbar(el, e.clientX, e.clientY);
          appState.selectedItem = el;
          renderCanvas();
          return;
        }}
      }}

      // Clicked outside elements
      closeFloatingToolbar();
    }});

    function openFloatingToolbar(el, clientX, clientY) {{
      const tb = document.getElementById('floatingToolbar');
      const rect = canvas.getBoundingClientRect();
      const scaleX = rect.width / canvas.width;
      const scaleY = rect.height / canvas.height;

      // Position relative to canvas viewport
      const screenX = rect.left + (el.x + el.w / 2) * scaleX;
      const screenY = rect.top + el.y * scaleY;

      tb.style.left = `${{screenX}}px`;
      tb.style.top = `${{screenY}}px`;
      tb.classList.add('open');

      document.getElementById('ftFieldLabel').textContent = el.label.toUpperCase() + ':';
      document.getElementById('ftTextInput').value = el.val;
      document.getElementById('ftSizeText').textContent = el.fontSize;
      document.getElementById('ftBoldBtn').classList.toggle('active', !!el.bold);
      document.getElementById('ftColorInput').value = el.color || '#000000';
    }}

    function closeFloatingToolbar() {{
      const tb = document.getElementById('floatingToolbar');
      if (tb) tb.classList.remove('open');
      if (appState.selectedItem) {{
        appState.selectedItem = null;
        renderCanvas();
      }}
    }}

    function onFloatingTextChange(newVal) {{
      if (!appState.selectedItem) return;
      const item = appState.selectedItem;
      const current = appState.people[appState.activePersonIndex];

      if (item.type === 'front-field') {{
        current.frontValues[item.id] = newVal;
        item.val = newVal;
      }} else if (item.type === 'back-field') {{
        current.backValues[item.id] = newVal;
        item.val = newVal;
      }} else if (item.type === 'back-date') {{
        current.backValues.date = newVal;
        item.val = newVal;
      }} else if (item.type === 'back-term') {{
        appState.layout.back.termsConfig.items[item.id] = newVal;
        item.val = newVal;
      }}
      renderFieldsUI();
      renderCanvas();
      debouncedSave();
    }}

    function hideFloatingSelectedItem() {{
      if (!appState.selectedItem) return;
      const item = appState.selectedItem;
      if (item.type === 'front-field') {{
        toggleFieldVisibility('front', item.id);
      }} else if (item.type === 'back-field') {{
        toggleFieldVisibility('back', item.id);
      }}
      closeFloatingToolbar();
    }}

    function adjustFloatingSize(delta) {{
      if (!appState.selectedItem) return;
      const item = appState.selectedItem;
      item.fontSize = Math.max(12, Math.min(80, (item.fontSize || 28) + delta));
      document.getElementById('ftSizeText').textContent = item.fontSize;

      if (item.type === 'front-field') {{
        appState.layout.front.textConfig.fontSize = item.fontSize;
      }} else if (item.type === 'back-field') {{
        const f = appState.layout.back.fields.find(x => x.id === item.id);
        if (f) f.size = item.fontSize;
      }} else if (item.type === 'back-date') {{
        appState.layout.back.signatureConfig.dateSize = item.fontSize;
      }} else if (item.type === 'back-term') {{
        appState.layout.back.termsConfig.size = item.fontSize;
      }}
      syncLayoutControls();
      renderCanvas();
      debouncedSave();
    }}

    function toggleFloatingBold() {{
      if (!appState.selectedItem) return;
      const item = appState.selectedItem;
      item.bold = !item.bold;
      document.getElementById('ftBoldBtn').classList.toggle('active', item.bold);

      if (item.type === 'front-field') {{
        appState.layout.front.textConfig.bold = item.bold;
      }} else if (item.type === 'back-field') {{
        const f = appState.layout.back.fields.find(x => x.id === item.id);
        if (f) f.bold = item.bold;
      }} else if (item.type === 'back-date') {{
        appState.layout.back.signatureConfig.dateBold = item.bold;
      }} else if (item.type === 'back-term') {{
        appState.layout.back.termsConfig.bold = item.bold;
      }}
      syncLayoutControls();
      renderCanvas();
      debouncedSave();
    }}

    function updateFloatingColor(color) {{
      if (!appState.selectedItem) return;
      const item = appState.selectedItem;
      item.color = color;

      if (item.type === 'front-field') {{
        appState.layout.front.textConfig.valueColor = color;
      }} else if (item.type === 'back-field') {{
        const f = appState.layout.back.fields.find(x => x.id === item.id);
        if (f) f.valColor = color;
      }} else if (item.type === 'back-date') {{
        appState.layout.back.signatureConfig.dateColor = color;
      }} else if (item.type === 'back-term') {{
        appState.layout.back.termsConfig.color = color;
      }}
      syncLayoutControls();
      renderCanvas();
      debouncedSave();
    }}

    window.addEventListener('mousemove', e => {{
      const pos = getCanvasPos(e);
      const person = appState.people[appState.activePersonIndex];

      // Handle Photo Dragging inside box
      if (isDraggingPhoto && person) {{
        const dx = pos.x - dragStartX;
        const dy = pos.y - dragStartY;
        dragStartX = pos.x;
        dragStartY = pos.y;
        person.photoOffsetX = (person.photoOffsetX || 0) + dx;
        person.photoOffsetY = (person.photoOffsetY || 0) + dy;
        renderCanvas();
      }}
    }});

    window.addEventListener('mouseup', () => {{
      if (isDraggingPhoto) {{
        isDraggingPhoto = false;
        canvas.style.cursor = 'default';
        debouncedSave();
      }}
    }});

    // Export High-Res PNG
    function generateCardDataURL(side, person) {{
      const offCanvas = document.createElement('canvas');
      const bgImg = appState.bg[side];
      offCanvas.width = bgImg ? bgImg.naturalWidth : 1024;
      offCanvas.height = bgImg ? bgImg.naturalHeight : (side === 'front' ? 763 : 710);
      drawCard(offCanvas.getContext('2d'), side, person, true);
      return offCanvas.toDataURL('image/png');
    }}

    function downloadCurrentPNG(side) {{
      const person = appState.people[appState.activePersonIndex];
      const name = (person && person.frontValues.name) ? person.frontValues.name.replace(/\\s+/g, '_') : `person_${{appState.activePersonIndex + 1}}`;
      const url = generateCardDataURL(side, person);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${{name}}_${{side}}_idcard.png`;
      a.click();
    }}

    // ================= BULK EDIT SPREADSHEET MODAL =================
    function openBulkEditModal() {{
      const head = document.getElementById('bulkTableHead');

      // Build Headers
      let ths = `<th>#</th><th>Photo</th>`;
      appState.layout.front.fields.forEach(f => {{
        const isHidden = (f.visible === false);
        ths += `<th>${{escapeHtml(f.label)}} ${{isHidden ? '<span style="color:#ef4444; font-size:10px;">(Hidden)</span>' : ''}}</th>`;
      }});
      appState.layout.back.fields.forEach(f => {{
        const isHidden = (f.visible === false);
        ths += `<th style="background:#f8fafc; color:#0369a1;">Back: ${{escapeHtml(f.label)}} ${{isHidden ? '<span style="color:#ef4444; font-size:10px;">(Hidden)</span>' : ''}}</th>`;
      }});
      ths += `<th style="background:#f8fafc; color:#0369a1;">Back: Date</th>`;
      ths += `<th>Actions</th>`;
      head.innerHTML = ths;

      renderBulkTableRows();
      document.getElementById('bulkEditModal').classList.add('open');
    }}

    function renderBulkTableRows() {{
      const body = document.getElementById('bulkTableBody');
      body.innerHTML = '';

      appState.people.forEach((p, idx) => {{
        const tr = document.createElement('tr');
        let rowHtml = `
          <td style="font-weight:700; text-align:center;">${{idx + 1}}</td>
          <td>
            <div class="photo-thumb-cell" title="Click to upload photo" onclick="triggerRowPhotoUpload(${{idx}})">
              ${{p.frontPhotoData ? `<img src="${{p.frontPhotoData}}" />` : `<span style="font-size:10px; color:#94a3b8;">+ Photo</span>`}}
            </div>
          </td>
        `;

        // Front fields
        appState.layout.front.fields.forEach(f => {{
          const val = p.frontValues[f.id] || '';
          rowHtml += `<td><input type="text" value="${{escapeHtml(val)}}" oninput="updatePersonValueDirect(${{idx}}, 'front', '${{f.id}}', this.value)" /></td>`;
        }});

        // Back fields
        appState.layout.back.fields.forEach(f => {{
          const val = p.backValues[f.id] || '';
          rowHtml += `<td><input type="text" value="${{escapeHtml(val)}}" oninput="updatePersonValueDirect(${{idx}}, 'back', '${{f.id}}', this.value)" /></td>`;
        }});

        // Back Date
        const dateVal = p.backValues.date || '21/11/2026';
        rowHtml += `<td><input type="text" value="${{escapeHtml(dateVal)}}" oninput="updatePersonDateDirect(${{idx}}, this.value)" /></td>`;

        // Actions
        rowHtml += `
          <td>
            <div style="display:flex; gap:4px;">
              <button class="btn btn-secondary btn-sm" onclick="duplicatePersonIndex(${{idx}})">Copy</button>
              <button class="btn btn-danger btn-sm" onclick="deletePersonIndex(${{idx}})">×</button>
            </div>
          </td>
        `;

        tr.innerHTML = rowHtml;
        body.appendChild(tr);
      }});
    }}

    function updatePersonValueDirect(personIdx, side, fieldId, value) {{
      const p = appState.people[personIdx];
      if (!p) return;
      if (side === 'front') p.frontValues[fieldId] = value;
      else p.backValues[fieldId] = value;
      renderPersonSelect();
      renderFieldsUI();
      renderCanvas();
      debouncedSave();
    }}

    function updatePersonDateDirect(personIdx, value) {{
      const p = appState.people[personIdx];
      if (p) {{
        p.backValues.date = value;
        renderCanvas();
        debouncedSave();
      }}
    }}

    function triggerRowPhotoUpload(personIdx) {{
      const fileInput = document.createElement('input');
      fileInput.type = 'file';
      fileInput.accept = 'image/*';
      fileInput.onchange = (e) => {{
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => {{
          const img = new Image();
          img.onload = () => {{
            appState.people[personIdx].frontPhoto = img;
            appState.people[personIdx].frontPhotoData = event.target.result;
            appState.people[personIdx].photoOffsetX = 0;
            appState.people[personIdx].photoOffsetY = 0;
            appState.people[personIdx].photoZoom = 1.0;
            renderBulkTableRows();
            renderCanvas();
            saveToStorage();
          }};
          img.src = event.target.result;
        }};
        reader.readAsDataURL(file);
      }};
      fileInput.click();
    }}

    function addNewPersonFromModal() {{
      addNewPerson();
      renderBulkTableRows();
    }}

    function addMultiplePeopleFromModal(count) {{
      for (let i = 0; i < count; i++) {{
        addNewPerson();
      }}
      renderBulkTableRows();
    }}

    function duplicatePersonIndex(idx) {{
      const copy = JSON.parse(JSON.stringify(appState.people[idx]));
      copy.id = Date.now();
      if (appState.people[idx].frontPhoto) copy.frontPhoto = appState.people[idx].frontPhoto;
      appState.people.splice(idx + 1, 0, copy);
      renderBulkTableRows();
      renderPersonSelect();
      saveToStorage();
    }}

    function deletePersonIndex(idx) {{
      if (appState.people.length <= 1) {{
        alert('At least one person is required.');
        return;
      }}
      appState.people.splice(idx, 1);
      appState.activePersonIndex = Math.min(appState.activePersonIndex, appState.people.length - 1);
      renderBulkTableRows();
      renderPersonSelect();
      renderFieldsUI();
      renderCanvas();
      saveToStorage();
    }}

    function closeBulkEditModal() {{
      document.getElementById('bulkEditModal').classList.remove('open');
      renderPersonSelect();
      renderFieldsUI();
      renderCanvas();
    }}

    // CSV Import / Export
    function exportCSV() {{
      const frontFields = appState.layout.front.fields;
      const backFields = appState.layout.back.fields;
      const headers = ['#', ...frontFields.map(f => f.label), ...backFields.map(f => 'Back_' + f.label), 'Back_Date'];
      
      const rows = appState.people.map((p, idx) => {{
        return [
          idx + 1,
          ...frontFields.map(f => `"${{(p.frontValues[f.id] || '').replace(/"/g, '""')}}"`),
          ...backFields.map(f => `"${{(p.backValues[f.id] || '').replace(/"/g, '""')}}"`),
          `"${{(p.backValues.date || '21/11/2026').replace(/"/g, '""')}}"`
        ].join(',');
      }});

      const csvContent = [headers.join(','), ...rows].join('\\n');
      const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
      const a = document.createElement('a');
      a.href = URL.createObjectURL(blob);
      a.download = 'id_card_people.csv';
      a.click();
    }}

    function importCSV(e) {{
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = (event) => {{
        const lines = event.target.result.split(/\\r?\\n/).filter(line => line.trim());
        if (lines.length < 2) {{ alert('CSV has no data rows.'); return; }}
        
        const dataRows = lines.slice(1);
        const frontFields = appState.layout.front.fields;
        const backFields = appState.layout.back.fields;

        dataRows.forEach(row => {{
          const cols = row.split(',').map(c => c.trim().replace(/^"|"$/g, '').replace(/""/g, '"'));
          if (cols.length < 2) return;
          const newP = {{
            id: Date.now() + Math.random(),
            frontPhoto: null,
            photoOffsetX: 0,
            photoOffsetY: 0,
            photoZoom: 1.0,
            frontValues: {{}},
            backValues: {{}}
          }};
          let colIdx = 1;
          frontFields.forEach(f => {{
            newP.frontValues[f.id] = cols[colIdx] || '';
            colIdx++;
          }});
          backFields.forEach(f => {{
            newP.backValues[f.id] = cols[colIdx] || '';
            colIdx++;
          }});
          newP.backValues.date = cols[colIdx] || '21/11/2026';
          appState.people.push(newP);
        }});

        renderBulkTableRows();
        renderPersonSelect();
        renderFieldsUI();
        renderCanvas();
        saveToStorage();
        alert(`Imported ${{dataRows.length}} people from CSV.`);
      }};
      reader.readAsText(file);
      e.target.value = '';
    }}

    // ================= A4 MULTI-PERSON PRINT SYSTEM =================
    function updatePrintConfig(key, value) {{
      appState.settings[key] = value;
      saveToStorage();
    }}

    function openPrintModal() {{
      generatePrintDOM();
      document.getElementById('printPreviewModal').classList.add('open');
    }}

    function closePrintModal() {{
      document.getElementById('printPreviewModal').classList.remove('open');
    }}

    // Generate high quality cards and assemble A4 sheets
    function generatePrintDOM() {{
      const previewContainer = document.getElementById('printPreviewPagesContainer');
      const printContainer = document.getElementById('printContainer');
      previewContainer.innerHTML = '';
      printContainer.innerHTML = '';

      const mode = appState.settings.printMode;
      const cardW = appState.settings.cardWidthMm || 80;
      const cardH = appState.settings.cardHeightMm || 45;
      const gapMm = appState.settings.printGapMm || 4;
      const rowGapMm = appState.settings.printRowGapMm || 5;
      const cutClass = appState.settings.cutGuide === 'solid' ? 'cut-guide-solid' : (appState.settings.cutGuide === 'dashed' ? 'cut-guide-dashed' : '');

      const peopleCount = appState.people.length;
      const rowsPerPage = 5;
      const totalPages = Math.ceil(peopleCount / rowsPerPage);

      document.getElementById('printPageCountSummary').textContent = `${{totalPages}} Page${{totalPages > 1 ? 's' : ''}} (${{peopleCount}} People, 5 per A4 sheet)`;

      for (let pIdx = 0; pIdx < totalPages; pIdx++) {{
        const pagePeople = appState.people.slice(pIdx * rowsPerPage, (pIdx + 1) * rowsPerPage);

        const vPage = document.createElement('div');
        vPage.className = 'virtual-a4-page';

        const rPage = document.createElement('div');
        rPage.className = 'print-a4-page';

        pagePeople.forEach(person => {{
          const frontData = generateCardDataURL('front', person);
          const backData = generateCardDataURL('back', person);

          let rowHtml = '';
          if (mode === 'both') {{
            rowHtml = `
              <img src="${{frontData}}" class="virtual-print-card print-card-img ${{cutClass}}" style="width: ${{cardW}}mm; height: ${{cardH}}mm;" alt="Front" />
              <div style="width: ${{gapMm}}mm; height: 100%;"></div>
              <img src="${{backData}}" class="virtual-print-card print-card-img ${{cutClass}}" style="width: ${{cardW}}mm; height: ${{cardH}}mm;" alt="Back" />
            `;
          }} else if (mode === 'front-only') {{
            rowHtml = `
              <img src="${{frontData}}" class="virtual-print-card print-card-img ${{cutClass}}" style="width: ${{cardW}}mm; height: ${{cardH}}mm;" alt="Front" />
            `;
          }} else {{
            rowHtml = `
              <img src="${{backData}}" class="virtual-print-card print-card-img ${{cutClass}}" style="width: ${{cardW}}mm; height: ${{cardH}}mm;" alt="Back" />
            `;
          }}

          const vRow = document.createElement('div');
          vRow.className = 'virtual-print-row';
          vRow.style.marginBottom = `${{rowGapMm}}mm`;
          vRow.innerHTML = rowHtml;
          vPage.appendChild(vRow);

          const rRow = document.createElement('div');
          rRow.className = 'print-row';
          rRow.style.marginBottom = `${{rowGapMm}}mm`;
          rRow.innerHTML = rowHtml;
          rPage.appendChild(rRow);
        }});

        previewContainer.appendChild(vPage);
        printContainer.appendChild(rPage);
      }}
    }}

    function triggerSystemPrint() {{
      window.print();
    }}

    window.addEventListener('beforeprint', () => {{
      generatePrintDOM();
    }});

    // ================= PROJECT STORAGE & PERSISTENCE =================
    let saveTimeout = null;
    function debouncedSave() {{
      clearTimeout(saveTimeout);
      saveTimeout = setTimeout(saveToStorage, 400);
    }}

    function saveToStorage() {{
      try {{
        const serialized = {{
          settings: appState.settings,
          layout: appState.layout,
          people: appState.people.map(p => ({{
            id: p.id,
            frontPhotoData: p.frontPhotoData || null,
            photoOffsetX: p.photoOffsetX || 0,
            photoOffsetY: p.photoOffsetY || 0,
            photoZoom: p.photoZoom || 1.0,
            frontValues: p.frontValues,
            backValues: p.backValues
          }})),
          authoritySignData: appState.authoritySignData || null
        }};
        localStorage.setItem('id_card_studio_state', JSON.stringify(serialized));
      }} catch (err) {{
        console.warn('Storage save failed:', err);
      }}
    }}

    function loadFromStorage() {{
      try {{
        const raw = localStorage.getItem('id_card_studio_state');
        if (!raw) return false;
        const parsed = JSON.parse(raw);
        if (parsed.settings) appState.settings = Object.assign({{}}, appState.settings, parsed.settings);
        if (parsed.layout) {{
          if (parsed.layout.front) {{
            appState.layout.front = Object.assign({{}}, appState.layout.front, parsed.layout.front);
            if (appState.layout.front.photoBox) {{
              if (appState.layout.front.photoBox.w > 300) {{
                appState.layout.front.photoBox = {{ x: 105, y: 295, w: 270, h: 350, visible: true, fit: 'contain' }};
              }}
            }}
            // If user previously removed fields or has old pa_no schema, restore to new requested default fields:
            const fList = appState.layout.front.fields;
            if (!Array.isArray(fList) || fList.length < 5 || !fList.some(f => f.id === 'pp_no') || !fList.some(f => f.id === 'country')) {{
              appState.layout.front.fields = JSON.parse(JSON.stringify(DEFAULT_FRONT_FIELDS));
            }} else {{
              appState.layout.front.fields.forEach(f => {{
                if (f.visible === undefined) f.visible = true;
              }});
            }}
          }}
          if (parsed.layout.back) {{
            const defBack = {{
              defaultFontSize: 26,
              defaultColor: '#001a70',
              photoBox: {{ x: 670, y: 350, w: 250, h: 75, visible: false, fit: 'contain' }},
              fields: JSON.parse(JSON.stringify(DEFAULT_BACK_FIELDS)),
              signatureConfig: {{
                dateLabel: 'Date.',
                dateX: 65,
                dateY: 425,
                dateSize: 24,
                dateColor: '#000000',
                dateBold: true,
                authorityLabel: 'Sign of Issuing Authority',
                authorityX: 650,
                authorityY: 425,
                authoritySize: 24,
                authorityColor: '#000000',
                authorityBold: true
              }},
              termsConfig: {{
                x: 65,
                startY: 495,
                rowGap: 42,
                size: 19,
                bold: false,
                color: '#000000',
                items: [
                  '1. Property of Govt of India.',
                  '2. Not transferable.',
                  '3. Loss is to be reported to issuing authority immediately.',
                  '4. Finder has no right to retain it and it is to be returned to the nearest Defense installation / Police station.'
                ]
              }}
            }};
            appState.layout.back = Object.assign({{}}, defBack, parsed.layout.back);
            if (!appState.layout.back.termsConfig || !Array.isArray(appState.layout.back.termsConfig.items)) {{
              appState.layout.back.termsConfig = defBack.termsConfig;
            }}
            if (!appState.layout.back.signatureConfig) {{
              appState.layout.back.signatureConfig = defBack.signatureConfig;
            }}
            if (!Array.isArray(appState.layout.back.fields) || 
                appState.layout.back.fields.length === 0 ||
                !appState.layout.back.fields.some(f => f.id === 'iafc_no')) {{
              appState.layout.back.fields = JSON.parse(JSON.stringify(DEFAULT_BACK_FIELDS));
            }} else {{
              appState.layout.back.fields.forEach(f => {{
                if (f.visible === undefined) f.visible = true;
              }});
            }}
          }}
        }}
        if (parsed.authoritySignData) {{
          appState.authoritySignData = parsed.authoritySignData;
          const img = new Image();
          img.onload = () => {{ appState.authoritySign = img; renderCanvas(); }};
          img.src = parsed.authoritySignData;
        }}
        if (Array.isArray(parsed.people) && parsed.people.length > 0) {{
          appState.people = parsed.people.map(p => {{
            const frontVals = p.frontValues || {{}};
            if (frontVals.pa_no && !frontVals.pp_no) {{
              frontVals.pp_no = frontVals.pa_no;
            }}
            const personObj = {{
              id: p.id,
              frontPhotoData: p.frontPhotoData || null,
              frontPhoto: null,
              photoOffsetX: p.photoOffsetX || 0,
              photoOffsetY: p.photoOffsetY || 0,
              photoZoom: p.photoZoom || 1.0,
              frontValues: Object.assign({{
                pp_no: '859342-K',
                name: 'SUBHASH CHANDRA',
                designation: 'JWO',
                country: 'INDIA',
                validity: 'TILL POSTED OUT'
              }}, frontVals),
              backValues: Object.assign({{
                sl_no: '0099',
                iafc_no: (p.backValues && (p.backValues.iafc_no || p.backValues.id_no)) || 'AFIC NO.',
                vim: (p.backValues && p.backValues.vim) || 'M-1294',
                validity: (p.backValues && p.backValues.validity) || 'TILL POSTED OUT',
                date: (p.backValues && p.backValues.date) || '15/08/2024'
              }}, p.backValues || {{}}, {{
                iafc_no: (p.backValues && (p.backValues.iafc_no || p.backValues.id_no)) || 'AFIC NO.'
              }})
            }};
            if (p.frontPhotoData) {{
              const pImg = new Image();
              pImg.onload = () => {{ personObj.frontPhoto = pImg; renderCanvas(); }};
              pImg.src = p.frontPhotoData;
            }}
            return personObj;
          }});
        }}
        return true;
      }} catch (err) {{
        console.warn('Storage load failed:', err);
        return false;
      }}
    }}

    // ================= STARTUP INITIALIZATION =================
    window.addEventListener('DOMContentLoaded', () => {{
      loadFromStorage();
      initBackgrounds(() => {{
        renderPersonSelect();
        renderFieldsUI();
        switchSide('front');
      }});
    }});
  </script>
</body>
</html>
'''

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('id-card-generator.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Generated index.html and id-card-generator.html ({len(html_content)} bytes)")
