# def sorted_rows_by_count(self):
#     rows = []

#     for k in sorted(self.row.keys()):
#         rows.append([k, self.row[k]])

#     for i in range(len(rows)-1):
#         for j in range(i+1, len(rows)):
#             if rows[i][1]['count'] > rows[j][1]['count']:
#                 rows[i], rows[j] = rows[j], rows[i]
#             elif rows[i][1]['count'] == rows[j][1]['count']:
#                 if min(rows[i][1]['ind']) > min(rows[j][1]['ind']):
#                     rows[i], rows[j] = rows[j], rows[i]
#     return rows

# def jpos(self, i, j, rows=None):
#     if rows is not None:
#         found = False

#         for t, t1 in enumerate(rows[i][1]['ind']):
#             if t1 == j:
#                 found = True
#                 break

#         return t
#     else:
#         return -1

# def divide_row2(self, row, k):
#     Assert(k != 0, 'k == 0', cf())

#     if k == 1:
#         return

#     if k == -1:
#         for j_pos, j in enumerate(row[i]['ind']):
#             row[i]['items'][j_pos] = -row[i]['items'][j_pos]
#     else:
#         for j_pos, j in enumerate(row['items']):
#             row['items'][j_pos] /= k

#     return
