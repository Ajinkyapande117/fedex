
#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <tuple>
#include <string>
#include <algorithm>
#include <omp.h>
#include <chrono>

using namespace std;

struct ULD {
    string identifier;
    int length, width, height, weightLimit;
};

struct Package {
    string identifier;
    int length, width, height, weight;
    char type; // 'P' for Priority, 'E' for Economy
    int costOfDelay;
};

struct PackedPackage {
    string packageID, uldID;
    int x0, y0, z0; // Coordinates of one corner
    int x1, y1, z1; // Coordinates of opposite corner
};

vector<ULD> loadULDs(const string& filename) {
    vector<ULD> ulds;
    ifstream file(filename);
    if (!file) {
        cerr << "Error: Unable to open ULD file " << filename << endl;
        exit(1);
    }
    string line;
    getline(file, line); // Skip header
    while (getline(file, line)) {
        istringstream iss(line);
        string id;
        int length, width, height, weightLimit;
        char comma;
        iss >> id >> comma >> length >> comma >> width >> comma >> height >> comma >> weightLimit;
        ulds.push_back({id, length, width, height, weightLimit});
    }
    return ulds;
}

vector<Package> loadPackages(const string& filename) {
    vector<Package> packages;
    ifstream file(filename);
    if (!file) {
        cerr << "Error: Unable to open Packages file " << filename << endl;
        exit(1);
    }
    string line;
    getline(file, line); // Skip header
    while (getline(file, line)) {
        istringstream iss(line);
        string id, typeStr;
        int length, width, height, weight, costOfDelay = 0;
        char type, comma;
        iss >> id >> comma >> length >> comma >> width >> comma >> height >> comma >> weight >> comma >> typeStr;
        type = (typeStr == "Priority" ? 'P' : 'E');
        if (type == 'E') iss >> comma >> costOfDelay;
        packages.push_back({id, length, width, height, weight, type, costOfDelay});
    }
    return packages;
}

void writeOutput(const vector<PackedPackage>& packedPackages, const string& filename) {
    ofstream file(filename);
    if (!file) {
        cerr << "Error: Unable to write to output file " << filename << endl;
        exit(1);
    }
    file << "Package_ID,ULD_ID,X0,Y0,Z0,X1,Y1,Z1\n";
    for (const auto& packed : packedPackages) {
        file << packed.packageID << "," << packed.uldID << ","
             << packed.x0 << "," << packed.y0 << "," << packed.z0 << ","
             << packed.x1 << "," << packed.y1 << "," << packed.z1 << "\n";
    }
}

void packPackages(const vector<ULD>& ulds, vector<Package>& packages, int K, const string& outputFilename) {
    vector<PackedPackage> packedPackages;
    int totalCost = 0, totalPacked = 0, priorityULDCount = 0;

    // Sort packages by priority and size
    sort(packages.begin(), packages.end(), [](const Package& a, const Package& b) {
        if (a.type != b.type) return a.type > b.type;
        return (a.length * a.width * a.height) > (b.length * b.width * b.height);
    });

    #pragma omp parallel for schedule(dynamic) reduction(+:totalCost, totalPacked, priorityULDCount) shared(packedPackages)
    for (size_t i = 0; i < ulds.size(); ++i) {
        const auto& uld = ulds[i];
        int currentWeight = 0;
        bool hasPriority = false;
        vector<tuple<int, int, int, int, int, int>> occupiedPositions;

        for (auto& pkg : packages) {
            if (pkg.weight == -1) continue; // Skip already packed packages
            for (int r = 0; r < 6; ++r) { // Check all rotations
                int l = (r < 2) ? pkg.length : (r < 4 ? pkg.width : pkg.height);
                int w = (r % 2 == 0) ? pkg.width : pkg.height;
                int h = (r % 3 == 0) ? pkg.height : pkg.length;

                if (currentWeight + pkg.weight <= uld.weightLimit) {
                    for (int x = 0; x <= uld.length - l; ++x) {
                        for (int y = 0; y <= uld.width - w; ++y) {
                            for (int z = 0; z <= uld.height - h; ++z) {
                                // Add the package to the packed list
                                packedPackages.push_back({pkg.identifier, uld.identifier, x, y, z, x + l, y + w, z + h});
                                currentWeight += pkg.weight;
                                if (pkg.type == 'P') hasPriority = true;
                                pkg.weight = -1; // Mark as packed
                                totalPacked++;
                                goto nextPackage; // Exit loops for this package
                            }
                        }
                    }
                }
            }
            nextPackage: continue;
        }

        if (hasPriority) priorityULDCount++;
    }

    totalCost += priorityULDCount * K;
    for (const auto& pkg : packages) {
        if (pkg.weight != -1) totalCost += pkg.costOfDelay;
    }

    cout << "Total Cost: " << totalCost << endl;
    cout << "Total Packed Packages: " << totalPacked << endl;
    cout << "Priority ULD Count: " << priorityULDCount << endl;

    writeOutput(packedPackages, outputFilename);
}

int main() {
    auto start = chrono::high_resolution_clock::now();

    // Load ULDs and packages from input files
    vector<ULD> ulds = loadULDs("final\\ULD's\\uld.csv");
    vector<Package> packages = loadPackages("final\\pakages\\packages1.csv");

    // Specify the output file path
    string outputFile = "final\\outputs\\output.csv";

    // Pack the packages into ULDs
    int K = 40; // Cost for each ULD carrying priority packages
    packPackages(ulds, packages, K, outputFile);

    auto stop = chrono::high_resolution_clock::now();
    auto duration = chrono::duration_cast<chrono::milliseconds>(stop - start);

    cout << "Execution time: " << duration.count() << " ms" << endl;
    return 0;
}
