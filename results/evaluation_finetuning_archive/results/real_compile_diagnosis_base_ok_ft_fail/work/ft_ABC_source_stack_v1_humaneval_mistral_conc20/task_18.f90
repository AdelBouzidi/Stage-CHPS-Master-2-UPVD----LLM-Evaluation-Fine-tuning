program main
  implicit none
  character(len=100) :: string
  character(len=100) :: substring
  integer :: count
  integer :: i, j, len_str, len_sub

  read *, string
  read *, substring

  count = 0
  len_str = len_trim(string)
  len_sub = len_trim(substring)

  if (len_sub > len_str) then
    count = 0
  else
    do i = 1, len_str - len_sub + 1
      if (string(i:i+len_sub-1) == substring) then
        count = count + 1
      end if
    end do
  end if

  print *, count
end program main