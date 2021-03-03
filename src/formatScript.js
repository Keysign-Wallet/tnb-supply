import promisify from "promisify";
import { readCsv, writeCsv } from "./utils/csv.js";
import { tasksInputHeaders, projectTeamsInputHeaders } from "./csvs/headers.js";

import { fileURLToPath } from "url";
import path, { dirname } from "path";
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

let contributorsObject = {};

const runScript = async () => {
  //get and Store all contributors
  await storeContributors();

  //Add the Account Number to Each Task
  await formatTasks();

  //Replace TNB MEMBER with the user's account number
  await formatProjectTeams();
};

runScript();

async function storeContributors() {
  let contributorsArray = await readCsv(
    path.join(__dirname, "csvs/input/contributors.csv")
  );

  for (let i = 0; i < contributorsArray.length; i++) {
    const contributor = contributorsArray[i];
    contributorsObject[contributor.github_username.toLowerCase()] =
      contributor.account_number;
  }
}

async function formatTasks() {
  let tasks = await readCsv(path.resolve(__dirname, "csvs/input/tasks.csv"));

  // console.log(contributorsObject);
  tasks.map((task) => {
    if (contributorsObject[task.completed_by.toLowerCase()]) {
      task.account_number = contributorsObject[task.completed_by.toLowerCase()];
    }
    if (!task.bug_bounty) {
      task.bug_bounty = "TRUE";
    }
  });

  await writeCsv(
    path.resolve(__dirname, "csvs/input/tasks.csv"),
    tasksInputHeaders,
    tasks
  );
}

async function formatProjectTeams() {
  let projectTeams = await readCsv(
    path.resolve(__dirname, "csvs/input/project-teams.csv")
  );

  projectTeams.map((projectTeam) => {
    if (projectTeam.account_number.includes("TNB MEMBER")) {
      if (contributorsObject[projectTeam.github_username.toLowerCase()]) {
        projectTeam.account_number =
          contributorsObject[projectTeam.github_username];
      }
    }
  });

  await writeCsv(
    path.resolve(__dirname, "csvs/input/project-teams.csv"),
    projectTeamsInputHeaders,
    projectTeams
  );
}
