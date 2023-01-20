class DictUtil:

    def find_in_range(self, ranges, find):

        for range in ranges:
            condition = True
            for tag in ['from', 'to']:
                if (tag == 'from' and range[tag + "_inclusive"]):
                    condition = find >= range[tag]
                elif (tag == 'from' and not range[tag + "_inclusive"]):
                    condition = find > range[tag]
                elif (tag == 'to' and range[tag + "_inclusive"]):
                    condition = (range[tag] is None) or (find <= range[tag])
                elif (tag == 'to' and not range[tag + "_inclusive"]):
                    condition = (range[tag] is None) or (find < range[tag])
                if (not condition):
                    break
            if (condition):
                return range
                
        return None