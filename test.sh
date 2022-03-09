# : ${DIALOG_OK=0}
# : ${DIALOG_CANCEL=1}
# : ${DIALOG_HELP=2}
# : ${DIALOG_EXTRA=3}
# : ${DIALOG_ITEM_HELP=4}
# : ${DIALOG_ESC=255}

# lipsum="Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
# tmp_file=$(tempfile 2>/dev/null) || temp_file=/tmp/test$$
# trap "rm -f $tmp_file" 0 1 2 5 15

# dialog --title "Testing" --clear --inputbox "${lipsum}" 16 51 2> $tmp_file

# return_value=$?

# case $return_value in
#     $DIALOG_OK)
#         echo "Result: $(cat $tmp_file)";;
#     $DIALOG_CANCEL)
#         echo "Cancel pressed.";;
#     $DIALOG_HELP)
#         echo "Help pressed.";;
#     $DIALOG_EXTRA)
#         echo "Extra button pressed.";;
#     $DIALOG_ITEM_HELP)
#         echo "Item-help button pressed.";;
#     $DIALOG_ESC)
#         if test -s $tmp_file ; then
#             cat $tmp_file
#         else
#             echo "ESC pressed."
#         fi
#         ;;
# esac

# dialog --begin 5 70 --backtitle "Shirak v0.1.0" --title "Info" --clear --msgbox 'Greetings, mortal...' 16 56  2> /dev/null

output="/tmp/shit.txt"
>$output

function hello() {
    local name=${@-"Stranger"}

    dialog --backtitle "Shirak v0.1.0 | test" --title "Greetings" --clear --msgbox "Greetings, ${name}..." 10 41
}


trap "rm $output; exit" SIGHUP SIGINT SIGTERM


dialog --title "Input your name" --backtitle "Shirak v0.1.0 | test" --inputbox "Enter your name " 8 60 2>$output

response=$?

name=$(<$output)

case $response in
    0)
        hello ${name}
        ;;
    1)
        echo "Cancel pressed."
        ;;
    255)
        echo "[esc] pressed."
esac


rm $output