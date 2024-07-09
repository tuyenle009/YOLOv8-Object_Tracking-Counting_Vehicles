import math
import cv2
import numpy as np


class EuclideanDistTracker:
    def __init__(self):
        # Store the center positions of the objects
        self.center_points = {}
        # Keep the count of the IDs
        # each time a new object id detected, the count will increase by one
        self.id_count = 0

    def update(self, objects_rect):
        # Objects boxes and ids
        objects_bbs_ids = []

        # Get center point of new object
        for rect in objects_rect:
            x, y, w, h = rect
            cx = (x + x + w) // 2
            cy = (y + y + h) // 2

            # Find out if that object was detected already
            same_object_detected = False
            for id, pt in self.center_points.items():
                dist = math.hypot(cx - pt[0], cy - pt[1])

                if dist < 25:
                    self.center_points[id] = (cx, cy)
                    # print(self.center_points)
                    objects_bbs_ids.append([x, y, w, h, id])
                    same_object_detected = True
                    break

            # New object is detected we assign the ID to that object
            if same_object_detected is False:
                self.center_points[self.id_count] = (cx, cy)
                objects_bbs_ids.append([x, y, w, h, self.id_count])
                self.id_count += 1

        # Clean the dictionary by center points to remove IDS not used anymore
        new_center_points = {}
        for obj_bb_id in objects_bbs_ids:
            _, _, _, _, object_id = obj_bb_id
            center = self.center_points[object_id]
            new_center_points[object_id] = center

        # Update dictionary with IDs not used removed
        self.center_points = new_center_points.copy()
        return objects_bbs_ids

    #draw opacity rectangle
    def opacityRectangle(self, img, bbox, color):
        x, y, w, h = bbox
        x1, y1 = int(x - w / 2), int(y - h / 2)
        x2, y2 = x1 + w, y1 + h

        # Initialize blank mask image of same dimensions for drawing the shapes
        shapes = np.zeros_like(img, np.uint8)

        # Draw shapes
        cv2.rectangle(shapes, (x1, y1), (x2, y2), color, cv2.FILLED)

        # Generate output by blending image with shapes image, using the shapes
        # images also as mask to limit the blending to those parts
        out = img.copy()
        alpha = 0.5
        mask = shapes.astype(bool)
        out[mask] = cv2.addWeighted(img, alpha, shapes, 1 - alpha, 0)[mask]
        return out
