program vowels_count
  implicit none
  character(len=*) :: input
  integer :: result

  read *, input
  result = vowels_count(input)
  print *, result

contains

  integer function vowels_count(s)
    character(len=*), intent(in) :: s
    integer :: i, len
    character(len=1) :: c

    len = len_trim(s)
    vowels_count = 0

    do i = 1, len
      c = s(i:i)
      select case (c)
      case ('a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U')
        vowels_count = vowels_count + 1
      case ('y', 'Y')
        if (i == len) then
          vowels_count = vowels_count + 1
        end if
      end select
    end do

  end function vowels_count

end program vowels_count