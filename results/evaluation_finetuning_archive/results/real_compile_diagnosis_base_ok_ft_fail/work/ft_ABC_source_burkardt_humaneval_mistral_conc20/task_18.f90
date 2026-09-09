program count_substring
  implicit none
  character(len=100) :: string, substring
  integer :: count

  read *, string
  read *, substring
  call count_substring_occurrences(string, substring, count)
  print *, count

contains

  subroutine count_substring_occurrences(string, substring, count)
    implicit none
    character(len=*), intent(in) :: string
    character(len=*), intent(in) :: substring
    integer, intent(out) :: count
    integer :: i, len_str, len_sub

    len_str = len_trim(string)
    len_sub = len_trim(substring)

    if (len_sub > len_str) then
      count = 0
      return
    end if

    count = 0
    do i = 1, len_str - len_sub + 1
      if (string(i:i+len_sub-1) == substring) then
        count = count + 1
      end if
    end do
  end subroutine count_substring_occurrences

end program count_substring