const fs = require('fs');
const path = require('path');

// Define all the components needed
const components = [
  // Characters
  { dir: 'Characters', name: 'CharacterDetails' },
  { dir: 'Characters', name: 'EditCharacter' },
  { dir: 'Characters', name: 'CreateCharacter' },
  
  // Events
  { dir: 'Events', name: 'EventCalendar' },
  { dir: 'Events', name: 'EventDetails' },
  { dir: 'Events', name: 'CreateEvent' },
  { dir: 'Events', name: 'EditEvent' },
  
  // Users
  { dir: 'Users', name: 'UserProfile' },
  
  // Dashboard
  { dir: 'Dashboard', name: 'Dashboard' },
  { dir: 'Dashboard', name: 'MyCharacters' },
  { dir: 'Dashboard', name: 'MyEvents' },
  { dir: 'Dashboard', name: 'AccountSettings' },
];

// Template for a placeholder component
const getTemplate = (name) => `import React from 'react';

const ${name} = () => {
  return (
    <div>
      <h1>${name}</h1>
      <p>This is a placeholder for the ${name} page.</p>
    </div>
  );
};

export default ${name};
`;

// Create the component files
components.forEach(component => {
  const dirPath = path.join('frontend', 'src', 'pages', component.dir);
  const filePath = path.join(dirPath, `${component.name}.js`);
  
  // Create the directory if it doesn't exist
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
  
  // Create the file
  fs.writeFileSync(filePath, getTemplate(component.name));
  
  console.log(`Created ${filePath}`);
});

// Create index.js files for each directory
const dirs = ['Characters', 'Events', 'Users', 'Dashboard'];
dirs.forEach(dir => {
  const dirPath = path.join('frontend', 'src', 'pages', dir);
  const indexPath = path.join(dirPath, 'index.js');
  
  // Get all JS files in the directory except index.js
  const files = fs.readdirSync(dirPath)
    .filter(file => file.endsWith('.js') && file !== 'index.js')
    .map(file => file.replace('.js', ''));
  
  // Create the index file content
  let indexContent = files.map(file => `import ${file} from './${file}';`).join('\n');
  indexContent += '\n\nexport {\n';
  indexContent += files.map(file => `  ${file}`).join(',\n');
  indexContent += '\n};\n';
  
  // Write the index file
  fs.writeFileSync(indexPath, indexContent);
  
  console.log(`Created ${indexPath}`);
});

console.log('All placeholder components created successfully!'); 