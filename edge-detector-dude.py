#!/usr/bin/env python

import string
import os
import shutil
import tempfile
import getpass

import gtk
import gtk.glade

program_dir = './'
program_unix_name = 'edge-detector-dude'

class Application:
    def __init__(self):
        glade_file_path = os.path.join(program_dir, program_unix_name + '.glade')
        xml = gtk.glade.XML(glade_file_path, 'main_window')
        xml.signal_autoconnect(self)

        window = xml.get_widget('main_window')
        icon_path = os.path.join(program_dir, 'icon.png')
        window.set_icon_from_file(icon_path)

        self.info_statusbar = xml.get_widget('info_statusbar')
        self.context_id = self.info_statusbar.get_context_id('context')
        self.SetStatusText('You can double click on a file to process.')

        self.input_image = xml.get_widget('input_image')
        self.sobel_image = xml.get_widget('sobel_image')
        self.gradient_image = xml.get_widget('gradient_image')

        self.sobel_button = xml.get_widget('sobel_button')
        self.gradient_button = xml.get_widget('gradient_button')

        gtk.main()

    def SaveImage(self, image_name, source):
        dialog = gtk.FileChooserDialog('Save ' + image_name + ' Image As...',
            None,
            gtk.FILE_CHOOSER_ACTION_SAVE,
            (gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT,
            gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))

        retval = dialog.run()

        if retval == gtk.RESPONSE_ACCEPT:
            destination = dialog.get_filename()
            try:
                shutil.copy(source, destination)
            except Exception, e:
                s = 'File "' + destination + '" cannot be saved: ' +  e.strerror
                self.SetStatusText(s)
            else:
                s = 'File "' + destination + '" successfully saved.'
                self.SetStatusText(s)

        dialog.destroy()

    def SetStatusText(self, text):
        self.info_statusbar.pop(self.context_id)
        self.info_statusbar.push(self.context_id, text)

    # signal handlers

    def on_filechooserwidget_file_activated(self, widget):

        def escape_path(unescaped_path):
            escaped_path = ''
            for c in unescaped_path:
                if c == ' ':
                    escaped_path += '\\'
                escaped_path += c
            return escaped_path

        filename = widget.get_filename()
        index = filename.rfind('.')
        if index != -1:
            extension = filename[index:].lower()
        else:
            extension = ''

        username = getpass.getuser()
        tempdir = tempfile.gettempdir()
        mytempdir = os.path.join(tempdir, program_unix_name + '-' + username)
        sobel_filepath = os.path.join(mytempdir, 'sobel' + extension)
        gradient_filepath = os.path.join(mytempdir, 'gradient' + extension)
        program_path = os.path.join(program_dir, 'gradient')

        if not os.path.isdir(mytempdir):
            os.mkdir(mytempdir)

        command = program_path + ' ' + escape_path(filename) + ' ' + \
            escape_path(sobel_filepath) + ' ' + \
            escape_path(gradient_filepath)

        self.SetStatusText('Processing...')
        while gtk.events_pending():
            gtk.main_iteration(False)

        process = os.popen(command)
        output = string.join(process.readlines(), '').strip().replace('\n', ' ')
        exitcode = process.close()

        if exitcode == None:
            self.input_image.set_from_file(filename)
            self.sobel_image.set_from_file(sobel_filepath)
            self.gradient_image.set_from_file(gradient_filepath)

            self.SetStatusText('File "' + filename + '" successfully processed.')

            self.sobel_button.set_sensitive(True)
            self.gradient_button.set_sensitive(True)
            self.sobel_filepath = sobel_filepath
            self.gradient_filepath = gradient_filepath
        else:
            self.SetStatusText(output)

    def on_sobel_button_clicked(self, widget):
        self.SaveImage('Sobel Edge-Detected', self.sobel_filepath)

    def on_gradient_button_clicked(self, widget):
        self.SaveImage('Gradient-Directed', self.gradient_filepath)

    def on_main_window_destroy(self, widget):
        gtk.main_quit()

if __name__ == '__main__':
    Application()
