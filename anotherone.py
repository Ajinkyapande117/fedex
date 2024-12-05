import pandas as pd
from multiprocessing import Pool
from heapq import heappush, heappop

# ULD data
uld_data = [
    ("U1", 224, 150, 162, 2500),
    ("U2", 224, 318, 162, 2500),
    ("U3", 244, 318, 244, 2800),
    ("U4", 244, 318, 244, 2800),
    ("U5", 244, 318, 285, 3500),
    ("U6", 244, 31, 28, 3500)
]

# Package data
package_data = [
    ("P-1", 99, 53, 55, 61, False, 176),
("P-2", 56, 99, 81, 53, True, None),
("P-3", 42, 101, 51, 17, True, None),
("P-4", 108, 75, 56, 73, False, 138),
("P-5", 88, 58, 64, 93, False, 139),
("P-6", 91, 56, 84, 47, True, None),
("P-7", 88, 78, 93, 117, False, 102),
("P-8", 108, 105, 76, 142, False, 108),
("P-9", 73, 71, 88, 50, True, None),
("P-10", 88, 70, 85, 81, True, None),
("P-11", 55, 80, 81, 23, False, 96),
("P-12", 48, 80, 88, 27, False, 117),
("P-13", 55, 94, 87, 41, False, 73),
("P-14", 45, 46, 81, 27, False, 68),
("P-15", 84, 49, 60, 57, True, None),
("P-16", 48, 93, 63, 82, True, None),
("P-17", 83, 63, 57, 29, True, None),
("P-18", 68, 101, 95, 96, False, 65),
("P-19", 51, 87, 69, 73, False, 107),
("P-20", 88, 106, 56, 71, True, None),
("P-21", 105, 71, 105, 223, False, 116),
("P-22", 100, 92, 99, 191, False, 86),
("P-23", 51, 50, 110, 59, True, None),
("P-24", 81, 109, 55, 123, False, 69),
("P-25", 44, 77, 53, 37, False, 108),
("P-26", 69, 56, 73, 56, False, 130),
("P-27", 93, 62, 49, 18, False, 122),
("P-28", 81, 64, 95, 70, False, 139),
("P-29", 62, 86, 53, 23, False, 122),
("P-30", 88, 85, 102, 164, False, 70),
("P-31", 71, 49, 76, 67, False, 76),
("P-32", 70, 44, 98, 53, False, 124),
("P-33", 90, 89, 73, 132, False, 136),
("P-34", 87, 45, 81, 45, False, 77),
("P-35", 83, 72, 63, 96, False, 103),
("P-36", 86, 80, 78, 146, True, None),
("P-37", 59, 76, 51, 33, False, 131),
("P-38", 84, 96, 48, 21, False, 60),
("P-39", 96, 64, 61, 61, False, 111),
("P-40", 70, 45, 90, 78, False, 106),
("P-41", 104, 90, 68, 72, True, None),
("P-42", 62, 109, 41, 46, True, None),
("P-43", 51, 86, 108, 87, False, 109),
("P-44", 84, 40, 49, 28, False, 87),
("P-45", 91, 72, 81, 92, True, None),
("P-46", 71, 62, 94, 39, True, None),
("P-47", 86, 58, 104, 149, False, 67),
("P-48", 53, 65, 48, 33, False, 67),
("P-49", 69, 40, 100, 55, True, None),
("P-50", 73, 104, 64, 75, True, None),
("P-51", 57, 86, 97, 65, False, 67),
("P-52", 104, 88, 102, 96, False, 121),
("P-53", 44, 53, 106, 14, False, 74),
("P-54", 106, 51, 59, 20, False, 98),
("P-55", 95, 93, 77, 71, False, 78),
("P-56", 65, 68, 109, 77, False, 85),
("P-57", 83, 64, 59, 32, False, 137),
("P-58", 95, 102, 55, 126, False, 134),
("P-59", 85, 79, 49, 26, False, 111),
("P-60", 60, 85, 87, 23, False, 84),
("P-60", 60, 85, 87, 23, False, 84),
("P-61", 57, 109, 95, 130, False, 136),
("P-62", 43, 92, 88, 25, False, 84),
("P-63", 75, 69, 85, 111, False, 116),
("P-64", 100, 56, 104, 123, False, 62),
("P-65", 50, 78, 110, 56, False, 121),
("P-66", 50, 47, 86, 53, False, 72),
("P-67", 76, 57, 101, 34, False, 65),
("P-68", 92, 46, 81, 62, True, None),
("P-69", 84, 47, 54, 57, True, None),
("P-70", 61, 78, 88, 49, False, 70),
("P-71", 82, 62, 98, 105, True, None),
("P-72", 93, 56, 110, 63, False, 72),
("P-73", 50, 75, 89, 53, False, 95),
("P-74", 85, 60, 92, 74, False, 83),
("P-75", 90, 52, 89, 89, True, None),
("P-76", 51, 56, 102, 68, True, None),
("P-77", 67, 49, 76, 78, False, 112),
("P-78", 49, 87, 93, 81, False, 99),
("P-79", 54, 50, 84, 65, True, None),
("P-80", 81, 89, 102, 42, False, 78),
("P-81", 50, 92, 109, 58, False, 120),
("P-82", 66, 74, 97, 47, True, None),
("P-83", 76, 61, 108, 56, False, 107),
("P-84", 53, 79, 83, 61, False, 88),
("P-85", 90, 58, 111, 99, True, None),
("P-86", 55, 73, 98, 67, False, 106),
("P-87", 65, 60, 104, 72, True, None),
("P-88", 76, 85, 93, 34, False, 110),
("P-89", 50, 69, 107, 79, False, 115),
("P-90", 82, 73, 85, 61, False, 111),
("P-91", 51, 81, 95, 60, False, 99),
("P-92", 79, 56, 113, 90, True, None),
("P-93", 63, 68, 108, 84, False, 116),
("P-94", 85, 80, 99, 44, True, None),
("P-95", 53, 89, 107, 68, False, 110),
("P-96", 92, 70, 97, 51, False, 109),
("P-97", 78, 50, 101, 65, True, None),
("P-98", 55, 75, 106, 76, False, 104),
("P-99", 80, 60, 91, 62, True, None),
("P-100", 51, 69, 109, 58, False, 90),
("P-101", 60, 74, 112, 55, False, 93),
("P-102", 70, 62, 98, 86, False, 100),
("P-103", 77, 57, 93, 53, False, 110),
("P-104", 85, 80, 103, 90, True, None),
("P-105", 91, 79, 94, 63, False, 112),
("P-106", 88, 76, 106, 78, False, 108),
("P-107", 94, 56, 111, 56, True, None),
("P-108", 83, 60, 89, 64, False, 105),
("P-109", 59, 75, 103, 73, False, 95),
("P-110", 69, 74, 100, 80, False, 107),
("P-111", 85, 68, 91, 66, True, None),
("P-112", 53, 61, 90, 77, False, 109),
("P-113", 66, 83, 106, 64, False, 108),
("P-114", 92, 59, 107, 85, True, None),
("P-115", 81, 73, 104, 55, False, 94),
("P-116", 76, 64, 98, 66, False, 110),
("P-117", 61, 80, 105, 59, False, 99),
("P-118", 80, 79, 97, 51, True, None),
("P-119", 68, 85, 113, 70, False, 118),
("P-120", 79, 58, 100, 72, False, 105),
("P-121", 84, 63, 112, 75, False, 117),
("P-122", 90, 59, 108, 53, True, None),
("P-123", 74, 70, 99, 80, False, 120),
("P-124", 51, 80, 93, 65, True, None),
("P-125", 68, 56, 92, 77, False, 102),
("P-126", 82, 72, 113, 56, False, 95),
("P-127", 75, 65, 106, 87, True, None),
("P-128", 92, 66, 111, 60, False, 100),
("P-129", 50, 78, 110, 90, False, 104),
("P-130", 84, 64, 108, 79, True, None),
("P-131", 53, 71, 98, 61, False, 108),
("P-132", 60, 55, 101, 65, False, 94),
("P-133", 89, 73, 115, 85, False, 111),
("P-134", 74, 66, 107, 50, False, 117),
("P-135", 91, 58, 92, 70, True, None),
("P-136", 78, 60, 113, 63, False, 95),
("P-137", 50, 74, 103, 82, True, None),
("P-138", 69, 57, 99, 55, False, 111),
("P-139", 90, 59, 110, 93, False, 102),
("P-140", 50, 69, 94, 80, False, 97),
("P-141", 76, 72, 112, 65, True, None),
("P-142", 60, 80, 110, 49, False, 103),
("P-143", 85, 63, 115, 59, False, 110),
("P-144", 75, 50, 89, 74, False, 108),
("P-145", 91, 62, 102, 66, False, 116),
("P-146", 50, 74, 108, 79, True, None),
("P-147", 84, 70, 107, 51, False, 113),
("P-148", 90, 66, 113, 80, True, None),
("P-149", 53, 75, 95, 72, False, 118),
("P-150", 70, 88, 112, 68, False, 106),
("P-151", 85, 66, 91, 58, True, None),
("P-152", 74, 78, 106, 49, False, 108),
("P-153", 92, 60, 111, 73, False, 115),
("P-154", 50, 64, 96, 59, False, 107),
("P-155", 61, 79, 104, 63, False, 118),
("P-156", 81, 60, 110, 72, False, 103),
("P-157", 68, 84, 97, 66, True, None),
("P-158", 85, 74, 99, 89, False, 110),
("P-159", 77, 67, 102, 54, False, 104),
("P-160", 50, 88, 105, 66, False, 116),
("P-161", 91, 60, 98, 77, True, None),
("P-162", 84, 72, 108, 69, False, 107),
("P-163", 59, 53, 106, 68, False, 113),
("P-164", 80, 64, 92, 75, True, None),
("P-165", 75, 81, 110, 56, False, 112),
("P-166", 50, 62, 103, 72, False, 106),
("P-167", 92, 56, 99, 74, True, None),
("P-168", 63, 75, 98, 50, False, 115),
("P-169", 88, 60, 113, 81, False, 100),
("P-170", 50, 68, 111, 66, False, 120),
("P-171", 92, 77, 104, 70, False, 103),
("P-172", 80, 55, 95, 87, True, None),
("P-173", 50, 77, 106, 90, False, 118),
("P-174", 72, 64, 104, 56, False, None),
("P-175", 50, 82, 101, 63, False, 105),
("P-176", 85, 67, 110, 70, False, 116),
("P-177", 78, 75, 112, 55, False, 113),
("P-178", 91, 81, 108, 72, False, 106),
("P-179", 92, 73, 105, 61, True, None),
("P-180", 50, 62, 106, 59, False, 99),
("P-181", 70, 64, 97, 66, False, 110),
("P-182", 85, 72, 111, 50, True, None),
("P-183", 53, 78, 95, 75, False, 114),
("P-184", 68, 69, 104, 67, False, 116),
("P-185", 80, 66, 111, 58, False, 109),
("P-186", 50, 73, 108, 75, False, 113),
("P-187", 81, 76, 106, 69, False, 118),
("P-188", 76, 58, 104, 60, True, None),
("P-189", 90, 64, 99, 85, False, 107),
("P-190", 50, 71, 98, 79, False, 120),
("P-191", 61, 77, 104, 69, False, 111),
("P-192", 80, 63, 101, 56, True, None),
("P-193", 70, 80, 107, 72, False, 98),
("P-194", 85, 66, 108, 62, False, 106),
("P-195", 53, 79, 106, 54, False, 112),
("P-196", 75, 61, 112, 63, True, None),
("P-197", 92, 64, 99, 71, False, 108),
("P-198", 80, 70, 108, 56, False, 115),
("P-199", 50, 68, 111, 73, True, None),
("P-200", 91, 79, 109, 60, False, 110),
("P-201", 53, 84, 107, 58, False, 105),
("P-202", 92, 72, 104, 67, False, 116),
("P-203", 70, 69, 106, 56, False, 113),
("P-204", 80, 65, 109, 74, False, 111),
("P-205", 85, 78, 102, 63, True, None),
("P-206", 50, 63, 98, 60, False, 108),
("P-207", 91, 70, 107, 59, False, 115),
("P-208", 75, 80, 104, 52, False, 112),
("P-209", 50, 81, 103, 68, False, 109),
("P-210", 81, 69, 100, 65, False, 116),
("P-211", 70, 63, 108, 80, False, 107),
("P-212", 92, 74, 111, 61, True, None),
("P-213", 50, 77, 106, 72, False, 111),
("P-214", 80, 71, 99, 55, False, 113),
("P-215", 85, 59, 109, 69, False, 115),
("P-216", 92, 69, 102, 60, False, 106),
("P-217", 53, 72, 107, 64, False, 113),
("P-218", 75, 60, 108, 63, False, 110),
("P-219", 80, 69, 111, 54, True, None),
("P-220", 50, 82, 95, 77, False, 114),
("P-221", 70, 65, 103, 70, True, None),
("P-222", 85, 76, 112, 68, False, 118),
("P-223", 92, 70, 106, 56, False, 105),
("P-224", 50, 63, 108, 71, False, 119),
("P-225", 81, 74, 107, 80, False, 112),
("P-226", 76, 66, 111, 60, False, 110),
("P-227", 53, 81, 109, 70, False, 113),
("P-228", 85, 72, 103, 63, True, None),
("P-229", 50, 75, 106, 64, False, 115),
("P-230", 91, 80, 109, 56, False, 107),
("P-231", 70, 66, 102, 73, False, 111),
("P-232", 50, 63, 108, 59, False, 114),
("P-233", 85, 79, 107, 67, False, 113),
("P-234", 80, 71, 100, 72, False, 116),
("P-235", 92, 64, 104, 70, False, 110),
("P-236", 53, 80, 103, 65, True, None),
("P-237", 75, 60, 112, 76, False, 114),
("P-238", 50, 78, 110, 63, False, 107),
("P-239", 80, 69, 105, 59, False, 118),
("P-240", 91, 75, 108, 65, False, 106),
("P-241", 53, 71, 109, 72, False, 115),
("P-242", 76, 70, 107, 64, False, 113),
("P-243", 50, 63, 101, 78, False, 112),
("P-244", 92, 72, 111, 65, False, 116),
("P-245", 80, 60, 110, 62, False, 104),
("P-246", 70, 75, 106, 55, True, None),
("P-247", 50, 84, 108, 79, False, 107),
("P-248", 91, 80, 113, 66, False, 103),
("P-249", 85, 76, 101, 59, False, 112),
("P-250", 50, 77, 95, 80, True, None),
("P-251", 70, 62, 107, 74, False, 116),
("P-252", 92, 69, 104, 55, False, 110),
("P-253", 50, 82, 112, 66, False, 106),
("P-254", 76, 60, 107, 63, True, None),
("P-255", 70, 78, 105, 72, False, 113),
("P-256", 92, 68, 110, 70, False, 104),
("P-257", 50, 75, 111, 67, False, 115),
("P-258", 70, 64, 108, 62, False, 106),
("P-259", 50, 80, 109, 75, False, 112),
("P-260", 91, 73, 104, 81, False, 107),
("P-261", 75, 69, 101, 72, False, 113),
("P-262", 50, 67, 95, 64, False, 105),
("P-263", 80, 79, 110, 56, False, 111),
("P-264", 53, 72, 113, 61, False, 106),
("P-265", 92, 75, 108, 55, False, 109),
("P-266", 70, 66, 107, 50, False, 115),
("P-267", 85, 80, 106, 61, False, 111),
("P-268", 50, 82, 107, 69, False, 120),
("P-269", 91, 75, 105, 62, False, 113),
("P-270", 80, 77, 110, 56, True, None),
("P-271", 53, 68, 104, 61, False, 108),
("P-272", 75, 64, 111, 74, False, 115),
("P-273", 50, 79, 107, 72, False, 107),
("P-274", 92, 72, 102, 64, False, 112),
("P-275", 50, 67, 103, 71, False, 119),
("P-276", 70, 62, 108, 75, False, 110),
("P-277", 81, 70, 109, 58, False, 113),
("P-278", 92, 77, 107, 68, False, 120),
("P-279", 50, 80, 111, 61, False, 109),
("P-280", 70, 75, 102, 79, False, 115),
("P-281", 53, 68, 106, 55, False, 110),
("P-282", 50, 64, 100, 67, False, 114),
("P-283", 92, 69, 113, 74, False, 118),
("P-284", 81, 76, 109, 80, False, 105),
("P-285", 70, 73, 108, 75, True, None),
("P-286", 50, 75, 104, 63, False, 113),
("P-287", 53, 66, 110, 72, False, 107),
("P-288", 92, 81, 108, 70, False, 116),
("P-289", 50, 79, 107, 64, False, 111),
("P-290", 70, 75, 103, 69, False, 104),
("P-291", 85, 63, 111, 58, True, None),
("P-292", 50, 81, 106, 71, False, 115),
("P-293", 91, 72, 99, 75, False, 113),
("P-294", 50, 67, 108, 66, False, 119),
("P-295", 53, 70, 102, 60, False, 114),
("P-296", 76, 75, 101, 72, False, 112),
("P-297", 92, 74, 103, 63, False, 107),
("P-298", 70, 68, 106, 55, False, 115),
("P-299", 50, 75, 104, 64, False, 113),
("P-300", 80, 79, 102, 66, False, 118),
("P-301", 92, 70, 107, 59, False, 104),
("P-302", 70, 76, 104, 61, False, 119),
("P-303", 50, 65, 109, 60, False, 107),
("P-304", 53, 74, 110, 62, False, 106),
("P-305", 92, 81, 111, 59, False, 114),
("P-306", 70, 78, 105, 63, False, 116),
("P-307", 50, 80, 103, 74, False, 120),
("P-308", 85, 75, 111, 62, False, 112),
("P-309", 92, 79, 104, 60, False, 109),
("P-310", 50, 81, 107, 65, False, 113),
("P-311", 70, 74, 110, 69, False, 115),
("P-312", 92, 77, 106, 64, False, 111),
("P-313", 50, 76, 104, 70, False, 113),
("P-314", 53, 72, 110, 59, False, 120),
("P-315", 70, 78, 103, 68, False, 107),
("P-316", 85, 67, 105, 75, False, 116),
("P-317", 92, 81, 109, 72, False, 110),
("P-318", 50, 79, 111, 63, False, 113),
("P-319", 70, 69, 108, 77, False, 114),
("P-320", 92, 74, 105, 69, False, 112),
("P-321", 50, 77, 107, 68, False, 108),
("P-322", 53, 70, 102, 61, False, 109),
("P-323", 76, 79, 110, 65, False, 107),
("P-324", 92, 75, 103, 59, False, 115),
("P-325", 50, 70, 106, 62, False, 114),
("P-326", 70, 76, 109, 75, False, 113),
("P-327", 53, 74, 104, 67, False, 116),
("P-328", 80, 65, 111, 59, False, 118),
("P-329", 92, 77, 102, 70, False, 120),
("P-330", 50, 72, 105, 75, False, 110),
("P-331", 85, 69, 111, 64, False, 107),
("P-332", 92, 79, 109, 68, False, 113),
("P-333", 50, 77, 108, 66, False, 115),
("P-334", 70, 80, 111, 69, False, 116),
("P-335", 92, 81, 107, 61, False, 104),
("P-336", 50, 63, 102, 74, False, 106),
("P-337", 70, 67, 110, 56, False, 109),
("P-338", 53, 75, 107, 61, False, 118),
("P-339", 80, 79, 106, 72, False, 111),
("P-340", 92, 77, 102, 75, False, 115),
("P-341", 50, 64, 110, 63, False, 113),
("P-342", 85, 76, 103, 69, False, 116),
("P-343", 92, 70, 107, 78, False, 112),
("P-344", 50, 69, 111, 64, False, 107),
("P-345", 70, 66, 106, 68, False, 110),
("P-346", 92, 75, 108, 70, False, 115),
("P-347", 50, 63, 102, 61, False, 119),
("P-348", 85, 79, 105, 73, False, 113),
("P-349", 92, 79, 107, 60, False, 106),
("P-350", 50, 78, 103, 66, False, 112),
("P-351", 70, 72, 110, 74, False, 115),
("P-352", 92, 70, 104, 79, False, 111),
("P-353", 50, 77, 108, 69, False, 107),
("P-354", 80, 65, 102, 75, False, 116),
("P-355", 92, 66, 107, 63, False, 113),
("P-356", 50, 79, 104, 70, False, 114),
("P-357", 85, 80, 109, 58, False, 119),
("P-358", 70, 68, 106, 60, False, 115),
("P-359", 92, 76, 110, 75, False, 106),
("P-360", 50, 70, 107, 67, False, 112),
("P-361", 92, 75, 109, 68, False, 113),
("P-362", 50, 66, 111, 60, False, 107),
("P-363", 70, 72, 105, 63, False, 110),
("P-364", 92, 74, 108, 77, False, 116),
("P-365", 50, 77, 102, 68, False, 107),
("P-366", 70, 63, 106, 75, False, 114),
("P-367", 92, 68, 103, 66, False, 119),
("P-368", 50, 69, 110, 72, False, 107),
("P-369", 70, 77, 104, 68, False, 110),
("P-370", 50, 73, 109, 65, False, 116),
("P-371", 92, 79, 106, 70, False, 113),
("P-372", 50, 75, 107, 64, False, 115),
("P-373", 70, 64, 105, 79, False, 116),
("P-374", 92, 76, 108, 73, False, 114),
("P-375", 50, 80, 103, 67, False, 107),
("P-376", 92, 70, 107, 69, False, 110),
("P-377", 50, 72, 101, 75, False, 113),
("P-378", 70, 79, 108, 78, False, 114),
("P-379", 92, 66, 109, 67, False, 107),
("P-380", 50, 74, 110, 72, False, 115),
("P-381", 70, 72, 108, 65, False, 113),
("P-382", 92, 73, 107, 69, False, 116),
("P-383", 50, 75, 101, 78, False, 107),
("P-384", 92, 74, 106, 69, False, 112),
("P-385", 50, 77, 102, 71, False, 111),
("P-386", 70, 75, 107, 63, False, 116),
("P-387", 50, 74, 111, 70, False, 107),
("P-388", 92, 70, 102, 60, False, 115),
("P-389", 50, 68, 104, 72, False, 113),
("P-390", 70, 74, 109, 65, False, 111),
("P-391", 92, 75, 108, 71, False, 107),
("P-392", 50, 79, 106, 64, False, 113),
("P-393", 92, 79, 103, 76, False, 109),
("P-394", 50, 68, 111, 70, False, 114),
("P-395", 70, 72, 105, 65, False, 112),
("P-396", 92, 74, 102, 77, False, 115),
("P-397", 50, 77, 108, 69, False, 113),
("P-398", 92, 73, 103, 68, False, 119),
("P-399", 50, 75, 106, 70, False, 107),
("P-400", 70, 74, 109, 61, False, 115)
]

K = 40  # Delay for spreading priority packages into multiple ULDs

# Precompute ULD dimensions
uld_dimensions = {
    uld[0]: {
        "Length": uld[1],
        "Width": uld[2],
        "Height": uld[3],
        "Volume": uld[1] * uld[2] * uld[3],
        "Weight": uld[4]
    }
    for uld in uld_data
}

package_df = pd.DataFrame(
    package_data,
    columns=["Package_ID", "Length", "Width", "Height", "Weight", "Type", "Cost_of_Delay"]
)

def rotate_package(package):
    """Generate all possible rotations of a package."""
    rotations = [
        (package["Length"], package["Width"], package["Height"]),
        (package["Length"], package["Height"], package["Width"]),
        (package["Width"], package["Length"], package["Height"]),
        (package["Width"], package["Height"], package["Length"]),
        (package["Height"], package["Length"], package["Width"]),
        (package["Height"], package["Width"], package["Length"])
    ]
    return [r for r in rotations if r[0] <= uld_dimensions["U5"]["Length"] 
            and r[1] <= uld_dimensions["U5"]["Width"] 
            and r[2] <= uld_dimensions["U5"]["Height"]]

def spatial_partition(occupied_positions, grid_size):
    """Create a spatial grid for overlap checks."""
    grid = {}
    for uld, positions in occupied_positions.items():
        grid[uld] = {}
        for position in positions:
            x0, y0, z0 = position[0]
            x1, y1, z1 = position[1]
            for x in range(x0 // grid_size, (x1 // grid_size) + 1):
                for y in range(y0 // grid_size, (y1 // grid_size) + 1):
                    for z in range(z0 // grid_size, (z1 // grid_size) + 1):
                        grid[uld].setdefault((x, y, z), []).append(position)
    return grid

def is_overlapping_spatial(new_pos_start, new_pos_end, grid, uld_id):
    """Check overlap using spatial partitioning."""
    grid_size = 50
    new_cells = spatial_partition({uld_id: [(new_pos_start, new_pos_end)]}, grid_size)[uld_id]
    for cell in new_cells:
        if cell in grid[uld_id]:
            for pos in grid[uld_id][cell]:
                if is_overlapping(pos, (new_pos_start, new_pos_end)):
                    return True
    return False

def is_overlapping(pkg1, pkg2):
    """Basic overlap check."""
    (x0_1, y0_1, z0_1), (x1_1, y1_1, z1_1) = pkg1
    (x0_2, y0_2, z0_2), (x1_2, y1_2, z1_2) = pkg2

    overlap_x = not (x1_1 <= x0_2 or x1_2 <= x0_1)
    overlap_y = not (y1_1 <= y0_2 or y1_2 <= y0_1)
    overlap_z = not (z1_1 <= z0_2 or z1_2 <= z0_1)

    return overlap_x and overlap_y and overlap_z

def fit_packages_to_uld(uld_dimensions, package_df):
    """Allocate packages to ULDs with optimized overlap and space checks."""
    allocations = {uld: [] for uld in uld_dimensions.keys()}
    occupied_positions = {uld: [] for uld in uld_dimensions.keys()}

    package_df["Volume"] = package_df["Length"] * package_df["Width"] * package_df["Height"]
    package_df = package_df.sort_values(by=["Type", "Volume", "Weight"], ascending=[False, False, False])

    for _, package in package_df.iterrows():
        package_rotations = rotate_package(package)
        allocated = False

        for uld in sorted(uld_dimensions.keys(), key=lambda uld: uld_dimensions[uld]["Volume"], reverse=True):
            for rotation in package_rotations:
                p_length, p_width, p_height = rotation
                for x in range(uld_dimensions[uld]["Length"] - p_length + 1):
                    for y in range(uld_dimensions[uld]["Width"] - p_width + 1):
                        for z in range(uld_dimensions[uld]["Height"] - p_height + 1):
                            if not is_overlapping_spatial((x, y, z), (x + p_length, y + p_width, z + p_height), occupied_positions, uld):
                                allocations[uld].append((package["Package_ID"], (x, y, z), (x + p_length, y + p_width, z + p_height)))
                                allocated = True
                                break
                        if allocated:
                            break
                    if allocated:
                        break
                if allocated:
                    break
            if allocated:
                break
    return allocations

# Fit packages to ULDs
allocations_result = fit_packages_to_uld(uld_dimensions, package_df)

# Priority ULD Count
priority_package_ids = package_df[package_df["Type"] == True]["Package_ID"].tolist()
priority_uld_count = len(set([uld for uld in allocations_result if any(pkg[0] in priority_package_ids for pkg in allocations_result[uld])]))

# Output results
print(f"Number of ULDs with priority packages: {priority_uld_count}")
print(f"Cost Delay: {K * priority_uld_count}")
for uld, packages in allocations_result.items():
    for pkg_id, start, end in packages:
        print(f"Package {pkg_id} allocated to ULD {uld} from {start} to {end}.")