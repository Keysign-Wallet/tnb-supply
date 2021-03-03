import fs from "fs";
import neatCsv from "neat-csv";
import csvWriter from "csv-writer";
import { readFileSync } from "fs";

import util from "util";

export const readCsv = async (path) => {
  //   let readCsv = util.promisify(readFile);
  const data = readFileSync(path);

  const parsedData = await neatCsv(data);
  console.log(`read ${path}`);
  return parsedData;
};

const createCsvWriter = csvWriter.createObjectCsvWriter;
export const writeCsv = async (path, header, data) => {
  await createCsvWriter({
    path,
    header,
  }).writeRecords(data);
  console.log(`writing to ${path} complete`);
};
