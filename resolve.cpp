#include <iostream>
#include <vector>
#include <algorithm>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <tuple>
#include <cmath>
#include <omp.h>

using namespace std;

// Structures
struct Package {
    string identifier;
    int length, width, height, weight;
    char type;  // 'P' for Priority, 'E' for Economy
    int costOfDelay;
    bool packed = false;
    tuple<int, int, int> placement; // Placement coordinates

    int getVolume() const { return length * width * height; }
    double getDensity() const { return static_cast<double>(weight) / getVolume(); }
};

struct ULD {
    string identifier;
    int length, width, height, weightLimit;
    int currentWeight = 0;
    int currentVolume = 0;
    vector<tuple<int, int, int, Package>> packedPackages; // (x, y, z, Package)

    int getRemainingWeight() const { return weightLimit - currentWeight; }
    int getRemainingVolume() const { return length * width * height - currentVolume; }
};

// CSV line splitting function
vector<string> getNextLineAndSplitIntoTokens(istream& str) {
    vector<string> result;
    string line;
    getline(str, line);
    stringstream lineStream(line);
    string cell;

    while (getline(lineStream, cell, ',')) {
        result.push_back(cell);
    }

    if (!lineStream && cell.empty()) {
        result.push_back("");
    }

    return result;
}

// Loaders
vector<ULD> loadULDs(const string& filename) {
    vector<ULD> ulds;
    ifstream file(filename);
    if (!file) {
        cerr << "Error: Unable to open ULD file " << filename << endl;
        exit(1);
    }

    string header;
    getline(file, header); // Skip header line

    while (!file.eof()) {
        vector<string> tokens = getNextLineAndSplitIntoTokens(file);
        if (tokens.size() < 5) continue;

        string id = tokens[0];
        int length = stoi(tokens[1]);
        int width = stoi(tokens[2]);
        int height = stoi(tokens[3]);
        int weightLimit = stoi(tokens[4]);

        ulds.push_back({id, length, width, height, weightLimit});
    }

    return ulds;
}

vector<Package> loadPackages(const string& filename) {
    vector<Package> packages;
    ifstream file(filename);
    if (!file) {
        cerr << "Error: Unable to open Package file " << filename << endl;
        exit(1);
    }

    string header;
    getline(file, header); // Skip header line

    while (!file.eof()) {
        vector<string> tokens = getNextLineAndSplitIntoTokens(file);
        if (tokens.size() < 6) continue;

        string id = tokens[0];
        int length = stoi(tokens[1]);
        int width = stoi(tokens[2]);
        int height = stoi(tokens[3]);
        int weight = stoi(tokens[4]);
        char type = tokens[5] == "Priority" ? 'P' : 'E';
        int costOfDelay = (tokens.size() > 6 && type == 'E') ? stoi(tokens[6]) : 0;

        packages.push_back({id, length, width, height, weight, type, costOfDelay});
    }

    return packages;
}

bool intelligentPackagePlacement(ULD& uld, Package& pkg) {
    struct Box {
        int x, y, z, length, width, height;
    };

    static vector<Box> placedBoxes;

    // Helper to check overlap between two boxes
    auto doesOverlap = [](const Box& b1, const Box& b2) {
        return !(b1.x + b1.length <= b2.x ||
                 b2.x + b2.length <= b1.x ||
                 b1.y + b1.width <= b2.y ||
                 b2.y + b2.width <= b1.y ||
                 b1.z + b1.height <= b2.z ||
                 b2.z + b2.height <= b1.z);
    };

    // Maintain a list of available spaces
    static vector<tuple<int, int, int>> availableSpaces = {{0, 0, 0}};

    vector<tuple<int, int, int>> rotations = {
        {pkg.length, pkg.width, pkg.height},
        {pkg.width, pkg.height, pkg.length},
        {pkg.height, pkg.length, pkg.width},
        {pkg.length, pkg.height, pkg.width},
        {pkg.width, pkg.length, pkg.height},
        {pkg.height, pkg.width, pkg.length}
    };

    for (const auto& rotation : rotations) {
        int l = get<0>(rotation);
        int w = get<1>(rotation);
        int h = get<2>(rotation);

        // Ensure package fits within ULD constraints
        if (l > uld.length || w > uld.width || h > uld.height ||
            uld.currentWeight + pkg.weight > uld.weightLimit ||
            uld.currentVolume + (l * w * h) > (uld.length * uld.width * uld.height)) {
            continue;
        }

        for (auto it = availableSpaces.begin(); it != availableSpaces.end(); ++it) {
            int x = get<0>(*it);
            int y = get<1>(*it);
            int z = get<2>(*it);

            Box newBox = {x, y, z, l, w, h};

            // Check overlap with all placed packages
            bool overlap = false;
            for (const auto& placedBox : placedBoxes) {
                if (doesOverlap(newBox, placedBox)) {
                    overlap = true;
                    break;
                }
            }

            if (!overlap) {
                // Place the package and update ULD stats
                placedBoxes.push_back(newBox);
                uld.packedPackages.emplace_back(x, y, z, pkg);
                uld.currentWeight += pkg.weight;
                uld.currentVolume += l * w * h;
                pkg.placement = {x, y, z};

                // Update available spaces
                availableSpaces.erase(it);
                availableSpaces.push_back({x + l, y, z});
                availableSpaces.push_back({x, y + w, z});
                availableSpaces.push_back({x, y, z + h});

                return true;
            }
        }
    }

    return false;
}


class AdvancedPackingOptimizer {
private:
    vector<Package> packages;
    vector<ULD> ulds;
    int priorityCost;

    void sophisticatedPackageSort() {
        sort(packages.begin(), packages.end(), [](const Package& a, const Package& b) {
            if (a.type != b.type) return a.type > b.type;
            if (abs(a.getDensity() - b.getDensity()) > 0.001)
                return a.getDensity() > b.getDensity();
            return a.getVolume() > b.getVolume();
        });
    }
    void simplePackagePlacement() {
        // Separate priority and economy packages
        vector<Package> priorityPackages, economyPackages;
        for (auto& pkg : packages) {
            if (pkg.type == 'P') {
                priorityPackages.push_back(pkg);
            } else {
                economyPackages.push_back(pkg);
            }
        }

                // Sort ULDs by size (volume) in descending order
        sort(ulds.begin(), ulds.end(), [](const ULD& a, const ULD& b) {
            return (a.length * a.width * a.height) > (b.length * b.width * b.height);
        });

        // Sort priority packages by volume in descending order
        sort(priorityPackages.begin(), priorityPackages.end(), [](const Package& a, const Package& b) {
            return a.getVolume() > b.getVolume();
        });

        // Place priority packages in the largest ULDs
        for (auto& uld : ulds) {
            if (priorityPackages.empty()) break;
            
            auto it = priorityPackages.begin();
            while (it != priorityPackages.end()) {
                if (intelligentPackagePlacement(uld, *it)) {
                    it = priorityPackages.erase(it);
                } else {
                    ++it;
                }
            }
        }

        // Sort economy packages by volume in descending order
        sort(economyPackages.begin(), economyPackages.end(), [](const Package& a, const Package& b) {
            return a.getVolume() > b.getVolume();
        });

        // Place economy packages in remaining space
        for (auto& uld : ulds) {
            auto it = economyPackages.begin();
            while (it != economyPackages.end()) {
                if (intelligentPackagePlacement(uld, *it)) {
                    it = economyPackages.erase(it);
                } else {
                    ++it;
                }
            }
        }

        // Mark any unpacked packages
        for (auto& pkg : priorityPackages) {
            pkg.packed = false;
        }
        for (auto& pkg : economyPackages) {
            pkg.packed = false;
        }
    }

public:
    AdvancedPackingOptimizer(const vector<Package>& pkgs, const vector<ULD>& containers, int priorityCost)
        : packages(pkgs), ulds(containers), priorityCost(priorityCost) {}

    vector<ULD> optimize() {
        sophisticatedPackageSort();
        #pragma omp parallel for schedule(dynamic)
        for (size_t i = 0; i < packages.size(); ++i) {
            Package& pkg = packages[i];
            if (pkg.packed) continue;

            for (auto& uld : ulds) {
                if (intelligentPackagePlacement(uld, pkg)) {
                    #pragma omp critical
                    {
                        pkg.packed = true;
                        break;
                    }
                }
            }
        }

        return ulds;
    }

    int calculateTotalCost() {
        int totalCost = 0;
        int priorityULDCount = 0;
        int totalPackedPackages = 0;

        // Count priority ULDs and packed packages
        for (const auto& uld : ulds) {
            totalPackedPackages += uld.packedPackages.size();
            
            // Check for priority packages
            if (any_of(uld.packedPackages.begin(), uld.packedPackages.end(), 
                       [](const tuple<int, int, int, Package>& p) { return get<3>(p).type == 'P'; })) {
                priorityULDCount++;
            }
        }

        // Calculate cost components
        totalCost += priorityULDCount * priorityCost;

        // Add delay costs for unpacked packages
        for (const Package& pkg : packages) {
            if (!pkg.packed) {
                totalCost += pkg.costOfDelay;
            }
        }

        return totalCost;
    }

    void generateOutput(const string& filename) {
    ofstream outputFile(filename);
    if (!outputFile) {
        cerr << "Error opening output file!" << endl;
        return;
    }

    unordered_set<string> packedPackageIds;
    for (const auto& uld : ulds) {
        for (const auto& entry : uld.packedPackages) {
            int x = get<0>(entry);
            int y = get<1>(entry);
            int z = get<2>(entry);
            const Package& pkg = get<3>(entry);
            outputFile << pkg.identifier << "," << uld.identifier
                       << "," << x << "," << y << "," << z
                       << "," << pkg.length << "," << pkg.width << "," << pkg.height << "\n";
            packedPackageIds.insert(pkg.identifier);
        }
    }

    for (const auto& pkg : packages) {
        if (packedPackageIds.find(pkg.identifier) == packedPackageIds.end()) {
            outputFile << pkg.identifier << ",NONE,-1,-1,-1,-1,-1,-1\n";
        }
    }
}

};

int main() {
    string uldFile = "E:/Tech Meet - FedX/approaches/final/ULD/uld.csv";
    string packageFile = "E:/Tech Meet - FedX/approaches/final/pakages/packages1.csv";
    vector<ULD> ulds = loadULDs(uldFile);
    vector<Package> packages = loadPackages(packageFile);

    AdvancedPackingOptimizer optimizer(packages, ulds, 40);
    vector<ULD> packedULDs = optimizer.optimize();

    optimizer.generateOutput("output.csv");

    return 0;
}