#!/usr/bin/env node

/**
 * MISSION CONTROL — Migration Script
 *
 * Maps 41 original tool .jsx artifacts into Next.js App Router routes.
 * - Adds 'use client'; directive
 * - Wraps PRO-gated tools with ProGate component
 * - Creates route directories as needed
 *
 * Usage:
 *   node migrate.js --dry-run   # Preview changes
 *   node migrate.js             # Execute migration
 */

const fs = require('fs');
const path = require('path');

const DRY_RUN = process.argv.includes('--dry-run');
const ARTIFACTS_DIR = path.join(__dirname, 'artifacts');
const SRC_DIR = path.join(__dirname, 'src', 'app');

// Mapping: artifact filename → route path + gate level
const ARTIFACT_MAP = {
  // Harley-Davidson (7)
  'HD_DTC_Database_v2.jsx': { route: 'harley/dtc', gate: 'free' },
  'HD_Diagnostic_Flowcharts_v2.jsx': { route: 'harley/flowcharts', gate: 'free' },
  'HD_Service_Reference_v2.jsx': { route: 'harley/service', gate: 'free' },
  'HD_Common_Problems_v2.jsx': { route: 'harley/problems', gate: 'free' },
  'HD_Wiring_Reference_v2.jsx': { route: 'harley/wiring', gate: 'pro' },
  'HD_Torque_Sequences_v2.jsx': { route: 'harley/torque', gate: 'pro' },
  'HD_Morning_Brief.jsx': { route: 'harley/morning-brief', gate: 'free' },

  // Automotive (5)
  'Auto_DTC_Database_v2.jsx': { route: 'auto/dtc', gate: 'free' },
  'Auto_Diagnostic_Flowcharts_v2.jsx': { route: 'auto/flowcharts', gate: 'free' },
  'Auto_Recall_TSB_Database_v2.jsx': { route: 'auto/recalls', gate: 'free' },
  'Auto_Fluid_Color_Guide_v2.jsx': { route: 'auto/fluid-guide', gate: 'free' },
  'Auto_Morning_Brief.jsx': { route: 'auto/morning-brief', gate: 'free' },

  // Trucking (7)
  'Trucker_HOS_Tracker_v2.jsx': { route: 'trucking/hos', gate: 'free' },
  'Trucker_PreTrip_Checklist_v2.jsx': { route: 'trucking/pretrip', gate: 'free' },
  'Trucker_Profit_Calculator_v2.jsx': { route: 'trucking/profit', gate: 'free' },
  'Trucker_IFTA_Generator_v2.jsx': { route: 'trucking/ifta', gate: 'free' },
  'Trucker_Axle_Weight_Calc_v2.jsx': { route: 'trucking/axle-weight', gate: 'free' },
  'Trucker_Calculator_Suite_v2.jsx': { route: 'trucking/calculators', gate: 'free' },
  'Trucker_Morning_Brief.jsx': { route: 'trucking/morning-brief', gate: 'free' },

  // E-Bike (7)
  'EBike_Error_Code_Database_v2.jsx': { route: 'ebike/errors', gate: 'free' },
  'EBike_Diagnostic_Flowcharts_v2.jsx': { route: 'ebike/flowcharts', gate: 'free' },
  'EBike_Battery_Range_Calculator_v2.jsx': { route: 'ebike/battery', gate: 'free' },
  'EBike_Class_Law_Reference_v2.jsx': { route: 'ebike/laws', gate: 'free' },
  'EBike_Wiring_Reference_v2.jsx': { route: 'ebike/wiring', gate: 'pro' },
  'EBike_Build_Calculator_v2.jsx': { route: 'ebike/build', gate: 'free' },
  'EBike_Morning_Brief.jsx': { route: 'ebike/morning-brief', gate: 'free' },

  // Scooter (5)
  'Scooter_Error_Code_Database_v2.jsx': { route: 'scooter/errors', gate: 'free' },
  'Scooter_Diagnostic_Flowcharts_v2.jsx': { route: 'scooter/flowcharts', gate: 'free' },
  'Scooter_Maintenance_Guide_v2.jsx': { route: 'scooter/maintenance', gate: 'free' },
  'Scooter_Comparison_Calculator_v2.jsx': { route: 'scooter/compare', gate: 'free' },
  'Scooter_Morning_Brief.jsx': { route: 'scooter/morning-brief', gate: 'free' },

  // Universal Tools (10)
  'Parts_Locator.jsx': { route: 'tools/parts', gate: 'free' },
  'Unit_Converter_v2.jsx': { route: 'tools/converter', gate: 'free' },
  'Fuel_Log_Tracker_v2.jsx': { route: 'tools/fuel-log', gate: 'free' },
  'Tire_Size_Calculator_v2.jsx': { route: 'tools/tire-calc', gate: 'free' },
  'Maintenance_Cost_Estimator_v2.jsx': { route: 'tools/maintenance-cost', gate: 'free' },
  'Fuel_Economy_Calculator_v2.jsx': { route: 'tools/fuel-economy', gate: 'free' },
  'OBD_Live_Data_Reference_v2.jsx': { route: 'tools/obd-reference', gate: 'free' },
  'Emergency_Roadside_Guide_v2.jsx': { route: 'tools/emergency', gate: 'free' },
  'Maintenance_Schedule_Builder_v2.jsx': { route: 'tools/schedule-builder', gate: 'free' },
  'Service_History_Export_v2.jsx': { route: 'tools/service-export', gate: 'pro' },
};

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`  📁 Created: ${dirPath}`);
  }
}

function wrapWithProGate(content, featureName) {
  // Add ProGate import if not present
  const importLine = "import ProGate from '@/components/ProGate';";

  // Find the default export
  const exportMatch = content.match(/export\s+default\s+function\s+(\w+)/);
  if (!exportMatch) {
    console.warn(`  ⚠️  Could not find default export to wrap`);
    return content;
  }

  const componentName = exportMatch[1];

  // Rename the component and create a wrapper
  let modified = content.replace(
    `export default function ${componentName}`,
    `function ${componentName}Inner`
  );

  // Add the wrapper at the end
  modified += `

export default function ${componentName}() {
  return (
    <ProGate requiredTier="pro" featureName="${featureName}">
      <${componentName}Inner />
    </ProGate>
  );
}
`;

  // Add import at top (after 'use client' if present)
  if (modified.includes("'use client'")) {
    modified = modified.replace("'use client';", `'use client';\n\n${importLine}`);
  } else {
    modified = `${importLine}\n\n${modified}`;
  }

  return modified;
}

function migrate() {
  console.log(`\n🚀 Mission Control Migration Script`);
  console.log(`   Mode: ${DRY_RUN ? 'DRY RUN (no changes)' : 'EXECUTE'}\n`);

  if (!fs.existsSync(ARTIFACTS_DIR)) {
    console.error(`❌ Artifacts directory not found: ${ARTIFACTS_DIR}`);
    console.error(`   Create it and place your 41 .jsx files inside.`);
    process.exit(1);
  }

  const files = fs.readdirSync(ARTIFACTS_DIR).filter((f) => f.endsWith('.jsx'));
  console.log(`📦 Found ${files.length} artifact files in ${ARTIFACTS_DIR}\n`);

  let migrated = 0;
  let skipped = 0;
  let errors = 0;

  for (const [filename, config] of Object.entries(ARTIFACT_MAP)) {
    const srcPath = path.join(ARTIFACTS_DIR, filename);
    const destDir = path.join(SRC_DIR, config.route);
    const destPath = path.join(destDir, 'page.jsx');

    if (!fs.existsSync(srcPath)) {
      console.log(`  ⏭️  Skip: ${filename} (not found in artifacts/)`);
      skipped++;
      continue;
    }

    if (DRY_RUN) {
      console.log(`  [DRY RUN] Would move: ${filename} → src/app/${config.route}/page.jsx ${config.gate === 'pro' ? '(PRO gated)' : ''}`);
      migrated++;
      continue;
    }

    try {
      // Read file
      let content = fs.readFileSync(srcPath, 'utf-8');

      // Add 'use client' if missing
      if (!content.startsWith("'use client'")) {
        content = `'use client';\n\n${content}`;
      }

      // Wrap with ProGate if needed
      if (config.gate === 'pro') {
        const featureName = filename.replace(/_v2\.jsx|\.jsx/g, '').replace(/_/g, ' ');
        content = wrapWithProGate(content, featureName);
      }

      // Create directory and write file
      ensureDir(destDir);
      fs.writeFileSync(destPath, content);
      console.log(`  ✅ ${filename} → src/app/${config.route}/page.jsx ${config.gate === 'pro' ? '🔒 PRO' : ''}`);
      migrated++;
    } catch (err) {
      console.error(`  ❌ Error migrating ${filename}: ${err.message}`);
      errors++;
    }
  }

  console.log(`\n📊 Results:`);
  console.log(`   ✅ Migrated: ${migrated}`);
  console.log(`   ⏭️  Skipped: ${skipped}`);
  console.log(`   ❌ Errors: ${errors}`);
  console.log(`   📁 Total mapped: ${Object.keys(ARTIFACT_MAP).length}\n`);

  if (DRY_RUN) {
    console.log(`💡 Run without --dry-run to execute the migration.\n`);
  }
}

migrate();
