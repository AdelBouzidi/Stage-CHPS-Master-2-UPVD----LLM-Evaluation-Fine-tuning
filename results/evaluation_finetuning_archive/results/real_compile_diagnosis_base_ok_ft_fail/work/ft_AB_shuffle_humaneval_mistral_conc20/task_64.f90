program vowels_count
  implicit none
  character(len=*) :: input
  integer :: count
  character(len=len(input)) :: s
  integer :: i

  read *, input
  s = trim(input)
  count = 0
  do i = 1, len_trim(s)
    select case (s(i:i))
    case ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
      count = count + 1
    case ('y', 'Y')
      if (i == len_trim(s)) then
        count = count + 1
      end if
    end select
  end do

  print *, count

end program vowels_count